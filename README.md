# 🎓 Student Task Manager

A full-stack task management application designed specifically for students to organize their academic and personal tasks efficiently.
This application features a secure, multi-user environment where students can manage their workload with advanced tools.

## ✨ Key Features

- **Secure User Authentication:** Full registration and login system with password hashing and session management to protect user data.
- **Complete Task Management (CRUD):**
  - **Create:** Add new tasks with detailed information.
  - **Read:** View a dynamic list of all personal tasks.
  - **Update:** Edit task details and toggle completion status (mark as complete/unmark).
  - **Delete:** Permanently remove tasks.
- **Rich Task Details:** Each task supports:
  - Detailed notes.
  - A priority level (High, Medium, Low).
  - A custom category (e.g., "Math", "History").
  - A due date.
- **File Attachments:** Users can upload a relevant file (PDF, image, etc.) to each task and download it securely.
- **Dynamic Dashboard:** The main dashboard provides a real-time statistical overview of the user's workload, including total tasks, completed tasks, and active tasks by priority level.
- **Secure & Private:** The backend is built with security in mind, ensuring users can only view, modify, and download their own tasks and files.

## 🛠️ Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Database:** SQLite
- **Tools:** Git, GitHub, Postman

## 🚀 Local Setup & Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/](https://github.com/)[YOUR-GITHUB-USERNAME]/student-task-manager.git
    cd student-task-manager
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Create and install dependencies:**
    First, you need to create the `requirements.txt` file by running the following command in your activated terminal:

    ```bash
    pip freeze > requirements.txt
    ```

    Then, install the packages:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**

    ```bash
    flask shell
    ```

    Then, inside the shell, run:

    ```python
    from app import db
    db.create_all()
    exit()
    ```

5.  **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000/`.

## 🔮 Future Improvements

- [ ] Allow multiple file uploads per task.
- [ ] Implement a calendar view for tasks with due dates.
- [ ] Add a daily "streak" feature to encourage productivity.
- [ ] Implement email or browser notifications for upcoming deadlines.

## ✍️ Author

- **Eswar** - [https://github.com/Eswar-15/student-task-manager]
