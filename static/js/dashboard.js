document.addEventListener("DOMContentLoaded", () => {
  const taskListContainer = document.getElementById("task-list-container");
  const addTaskForm = document.getElementById("add-task-form");
  const editModal = document.getElementById("edit-modal");
  const editForm = document.getElementById("edit-task-form");
  let currentTasks = []; // Variable to store tasks for easy access

  // --- FUNCTIONS TO FETCH AND RENDER DATA ---

  const fetchStats = async () => {
    const response = await fetch("/api/stats");
    if (!response.ok) return;
    const stats = await response.json();
    document.getElementById("stats-total").textContent = stats.total;
    document.getElementById("stats-completed").textContent = stats.completed;
    document.getElementById("stats-high").textContent = stats.high;
    document.getElementById("stats-medium").textContent = stats.medium;
    document.getElementById("stats-low").textContent = stats.low;
  };

  const fetchTasks = async () => {
    const response = await fetch("/api/tasks");
    if (!response.ok) return;
    const data = await response.json();
    currentTasks = data.tasks; // Save the latest tasks

    taskListContainer.innerHTML = "";
    if (currentTasks.length === 0) {
      taskListContainer.innerHTML = "<p>No tasks yet. Add one above!</p>";
    } else {
      currentTasks.forEach((task) => {
        const taskArticle = document.createElement("article");
        if (task.is_complete) {
          taskArticle.classList.add("completed-task");
        }

        taskArticle.innerHTML = `
                    <header><strong>${task.title}</strong></header>
                    <p>${task.notes || "<em>No notes.</em>"}</p>
                    <footer>
                        <div class="grid">
                            <div><strong>Priority:</strong> ${
                              task.priority
                            }</div>
                            <div><strong>Category:</strong> ${
                              task.category || "N/A"
                            }</div>
                            <div><strong>Due:</strong> ${
                              task.due_date
                                ? new Date(task.due_date).toLocaleDateString()
                                : "N/A"
                            }</div>
                        </div>
                        ${
                          task.attachment_filename
                            ? `<a href="/uploads/${task.attachment_filename}" target="_blank" role="button" class="secondary outline">View Attachment</a>`
                            : ""
                        }
                    </footer>
                    <div class="task-actions">
                        <button class="edit-btn" data-task-id="${
                          task.id
                        }">✏️ Edit</button>
                        <button class="complete-btn" data-task-id="${task.id}">
                            ${
                              task.is_complete
                                ? "🔄 Mark as To-Do"
                                : "✅ Mark as Complete"
                            }
                        </button>
                        <button class="delete-btn contrast" data-task-id="${
                          task.id
                        }">🗑️ Delete</button>
                    </div>
                `;
        taskListContainer.appendChild(taskArticle);
      });
    }
  };

  // --- EVENT LISTENERS ---

  if (addTaskForm) {
    addTaskForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(addTaskForm);
      const dateValue = formData.get("due_date");
      if (dateValue) {
        formData.set("due_date", new Date(dateValue).toISOString());
      }

      const response = await fetch("/api/tasks", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        addTaskForm.reset();
        fetchTasks();
        fetchStats();
      } else {
        alert("Error adding task.");
      }
    });
  }

  if (taskListContainer) {
    taskListContainer.addEventListener("click", async (e) => {
      const target = e.target;
      const taskId = target.dataset.taskId;

      // Handle Complete/Unmark
      if (target.classList.contains("complete-btn")) {
        const response = await fetch(`/api/tasks/${taskId}`, { method: "PUT" });
        if (response.ok) {
          fetchTasks();
          fetchStats();
        }
      }

      // Handle Delete
      if (target.classList.contains("delete-btn")) {
        if (confirm("Are you sure you want to delete this task?")) {
          const response = await fetch(`/api/tasks/${taskId}`, {
            method: "DELETE",
          });
          if (response.ok) {
            fetchTasks();
            fetchStats();
          }
        }
      }

      // Handle Edit button click (to open modal)
      if (target.classList.contains("edit-btn")) {
        const taskToEdit = currentTasks.find((task) => task.id == taskId);
        if (taskToEdit) {
          document.getElementById("edit-task-id").value = taskToEdit.id;
          document.getElementById("edit-title").value = taskToEdit.title;
          document.getElementById("edit-notes").value = taskToEdit.notes;
          document.getElementById("edit-priority").value = taskToEdit.priority;
          document.getElementById("edit-category").value = taskToEdit.category;
          document.getElementById("edit-due_date").value = taskToEdit.due_date
            ? taskToEdit.due_date.split("T")[0]
            : "";
          editModal.showModal();
        }
      }
    });
  }

  // Handle Edit form submission
  if (editForm) {
    editForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const taskId = document.getElementById("edit-task-id").value;
      const updatedData = {
        title: document.getElementById("edit-title").value,
        notes: document.getElementById("edit-notes").value,
        priority: document.getElementById("edit-priority").value,
        category: document.getElementById("edit-category").value,
        due_date: document.getElementById("edit-due_date").value
          ? new Date(
              document.getElementById("edit-due_date").value
            ).toISOString()
          : null,
      };

      const response = await fetch(`/api/tasks/${taskId}/edit`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updatedData),
      });

      if (response.ok) {
        editModal.close();
        fetchTasks();
      } else {
        alert("Failed to update task.");
      }
    });
  }

  // Handle closing the modal
  if (editModal) {
    const closeModalButton = editModal.querySelector(".close");
    closeModalButton.addEventListener("click", () => {
      editModal.close();
    });
  }

  // --- INITIAL PAGE LOAD ---
  fetchStats();
  fetchTasks();
});
