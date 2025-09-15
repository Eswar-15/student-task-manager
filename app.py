import os # NEW import for file paths
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename # NEW import for secure filenames
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# --- NEW: Configuration for file uploads ---
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# --- 10MB LIMIT ---
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # Sets the limit to 10 MB
# --- End of New Configuration ---

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    # ... (code is the same) ...
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)


# --- UPDATED Task Model ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    attachment_filename = db.Column(db.String(300), nullable=True) # NEW
    is_complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# --- create task ---
@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    # --- DEBUGGING LINES ---
    print("Form data received:", request.form)
    print("Files received:", request.files)
    # --- END DEBUGGING ---
    
    # Get text data from the form part of the request
    title = request.form.get('title')
    priority = request.form.get('priority')
    notes = request.form.get('notes')
    category = request.form.get('category')
    due_date_str = request.form.get('due_date')

    if not title or not priority:
        return jsonify({'message': 'Title and priority are required!'}), 400

    due_date = None
    if due_date_str:
        due_date = datetime.fromisoformat(due_date_str)
    
    filename = None
    if 'attachment' in request.files:
        file = request.files['attachment']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    new_task = Task(
        title=title,
        priority=priority,
        notes=notes,
        category=category,
        due_date=due_date,
        attachment_filename=filename,
        user_id=current_user.id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task created successfully!'}), 201

# --- UPDATED Get Tasks Route ---
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = current_user.tasks
    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'notes': task.notes,
            'priority': task.priority,
            'category': task.category,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'is_complete': task.is_complete,
            'attachment_filename': task.attachment_filename # NEW
        }
        task_list.append(task_data)
    return jsonify({'tasks': task_list})


# ... (The rest of your code: login, register, update, delete, stats, etc. remains the same) ...
@app.route('/')
def index():
    # If the user is already logged in, send them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    # If they are not logged in, send them to the login page
    else:
        return redirect(url_for('login_page'))

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created successfully!'})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password!'}), 401
    login_user(user)
    return jsonify({'message': 'Login successful!'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task or task.owner != current_user:
        return jsonify({'message': 'Task not found or permission denied!'}), 404
    task.is_complete = not task.is_complete # This will toggle the status
    db.session.commit()
    return jsonify({'message': 'Task marked as complete!'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task or task.owner != current_user:
        return jsonify({'message': 'Task not found or permission denied!'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully!'})

@app.route('/api/tasks/<int:task_id>/edit', methods=['PUT'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    if not task or task.owner != current_user:
        return jsonify({'message': 'Task not found or permission denied!'}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.notes = data.get('notes', task.notes)
    task.priority = data.get('priority', task.priority)
    task.category = data.get('category', task.category)
    
    due_date_str = data.get('due_date')
    if due_date_str:
        # Check for empty string before converting
        task.due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
    else:
        task.due_date = None

    db.session.commit()
    return jsonify({'message': 'Task updated successfully!'})

@app.route('/api/stats', methods=['GET'])
@login_required
def get_stats():
    total_tasks = Task.query.filter_by(owner=current_user).count()
    completed_tasks = Task.query.filter_by(owner=current_user, is_complete=True).count()
    high_priority = Task.query.filter_by(owner=current_user, priority='high', is_complete=False).count()
    medium_priority = Task.query.filter_by(owner=current_user, priority='medium', is_complete=False).count()
    low_priority = Task.query.filter_by(owner=current_user, priority='low', is_complete=False).count()
    return jsonify({'total': total_tasks, 'completed': completed_tasks, 'high': high_priority, 'medium': medium_priority, 'low': low_priority})

# --- NEW: Route to download/view uploaded files ---
@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    # This is a crucial security check to make sure a user can only access their own files.
    task = Task.query.filter_by(owner=current_user, attachment_filename=filename).first_or_404()
    
    # send_from_directory is a secure way to send files to the user.
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# --- ADD THE NEW LOGIN PAGE ROUTE HERE ---
@app.route('/login-page')
def login_page():
    return render_template('login.html')
# ----------------------------------------

# --- ADD THE NEW REGISTER PAGE ROUTE HERE ---
@app.route('/register-page')
def register_page():
    return render_template('register.html')
# ----------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)