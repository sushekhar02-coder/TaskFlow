
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [showForm, setShowForm] = useState(false);

  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");

  const [tasks, setTasks] = useState([]);
  const [projectId, setProjectId] = useState(null);

  const [quickDescription, setQuickDescription] = useState("");

  const [editingTask, setEditingTask] = useState(null);

  // -------------------------
  // LOAD PROJECTS AND TASKS
  // -------------------------
  useEffect(() => {
    loadProjects();
    loadTasks();
  }, []);

  // -------------------------
  // LOAD PROJECTS
  // -------------------------
  const loadProjects = async () => {
    try {
      const response = await fetch(`${API_URL}/projects`);

      if (!response.ok) {
        throw new Error("Could not load projects");
      }

      const projects = await response.json();

      if (projects.length > 0) {
        setProjectId(projects[0].id);
      } else {
        alert("No project found. Please create a project first.");
      }
    } catch (error) {
      console.error(error);
      alert("Could not connect to the backend.");
    }
  };

  // -------------------------
  // LOAD TASKS
  // -------------------------
  const loadTasks = async () => {
    try {
      const response = await fetch(`${API_URL}/tasks`);

      if (!response.ok) {
        throw new Error("Could not load tasks");
      }

      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error(error);
      alert("Could not load tasks from the database.");
    }
  };

  // -------------------------
  // CREATE TASK
  // -------------------------
  const handleSave = async () => {
    if (!title.trim()) {
      alert("Please enter a task title");
      return;
    }

    if (!projectId) {
      alert("No project is available.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: title.trim(),
          priority: priority,
          due_date: dueDate || null,
          project_id: projectId,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to create task");
      }

      setTasks((currentTasks) => [...currentTasks, data]);

      setTitle("");
      setPriority("medium");
      setDueDate("");
      setShowForm(false);

      alert("Task created successfully!");
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  // -------------------------
  // QUICK ADD TASK
  // -------------------------
  const handleQuickAdd = async () => {
    if (!quickDescription.trim()) {
      alert("Please enter a task description");
      return;
    }

    if (!projectId) {
      alert("No project is available.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/tasks/quick-add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          description: quickDescription.trim(),
          project_id: projectId,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to quick-add task");
      }

      setTasks((currentTasks) => [...currentTasks, data]);

      setQuickDescription("");

      alert("Quick task created successfully!");
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  // -------------------------
  // START EDITING
  // -------------------------
  const startEditing = (task) => {
    setEditingTask({
      id: task.id,
      title: task.title,
      priority: task.priority,
      due_date: task.due_date || "",
    });
  };

  // -------------------------
  // UPDATE TASK
  // -------------------------
  const handleUpdate = async () => {
    if (!editingTask.title.trim()) {
      alert("Please enter a task title");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/tasks/${editingTask.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: editingTask.title.trim(),
            priority: editingTask.priority,
            due_date: editingTask.due_date || null,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to update task");
      }

      setTasks((currentTasks) =>
        currentTasks.map((task) =>
          task.id === data.id ? data : task
        )
      );

      setEditingTask(null);

      alert("Task updated successfully!");
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  // -------------------------
  // DELETE TASK
  // -------------------------
  const handleDelete = async (id) => {
    try {
      const response = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to delete task");
      }

      setTasks((currentTasks) =>
        currentTasks.filter((task) => task.id !== id)
      );
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  // -------------------------
  // FRONTEND
  // -------------------------
  return (
    <div className="app-container">

      {/* HEADER */}
      <header className="app-header">
        <h1>TaskFlow</h1>
        <p>Manage your tasks easily.</p>

        {/* QUICK ADD */}
        <div className="quick-add">
          <h2>Quick Add</h2>

          <div className="quick-add-row">
            <input
              className="task-input"
              type="text"
              placeholder="e.g. urgent finish project tomorrow"
              value={quickDescription}
              onChange={(e) =>
                setQuickDescription(e.target.value)
              }
            />

            <button
              className="add-button"
              onClick={handleQuickAdd}
            >
              Quick Add Task
            </button>
          </div>
        </div>

        <br />

        {/* NORMAL ADD BUTTON */}
        <button
          className="add-button"
          onClick={() => setShowForm(true)}
        >
          Add Task
        </button>
      </header>

      {/* ADD TASK FORM */}
      {showForm && (
        <div className="task-form">
          <h2>Add New Task</h2>

          <input
            className="task-input"
            type="text"
            placeholder="Task title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <div className="form-row">

            <div className="form-group">
              <label>Priority:</label>

              <select
                className="task-select"
                value={priority}
                onChange={(e) =>
                  setPriority(e.target.value)
                }
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div className="form-group">
              <label>Due date:</label>

              <input
                className="task-date"
                type="date"
                value={dueDate}
                onChange={(e) =>
                  setDueDate(e.target.value)
                }
              />
            </div>

          </div>

          <div className="form-buttons">
            <button
              className="save-button"
              onClick={handleSave}
            >
              Save Task
            </button>

            <button
              className="cancel-button"
              onClick={() => setShowForm(false)}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* EDIT TASK FORM */}
      {editingTask && (
        <div className="task-form">
          <h2>Edit Task</h2>

          <input
            className="task-input"
            type="text"
            placeholder="Task title"
            value={editingTask.title}
            onChange={(e) =>
              setEditingTask({
                ...editingTask,
                title: e.target.value,
              })
            }
          />

          <div className="form-row">

            <div className="form-group">
              <label>Priority:</label>

              <select
                className="task-select"
                value={editingTask.priority}
                onChange={(e) =>
                  setEditingTask({
                    ...editingTask,
                    priority: e.target.value,
                  })
                }
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>

            <div className="form-group">
              <label>Due date:</label>

              <input
                className="task-date"
                type="date"
                value={editingTask.due_date}
                onChange={(e) =>
                  setEditingTask({
                    ...editingTask,
                    due_date: e.target.value,
                  })
                }
              />
            </div>

          </div>

          <div className="form-buttons">

            <button
              className="update-button"
              onClick={handleUpdate}
            >
              Update Task
            </button>

            <button
              className="cancel-button"
              onClick={() => setEditingTask(null)}
            >
              Cancel
            </button>

          </div>
        </div>
      )}

      {/* TASK LIST */}
      <section className="tasks-section">

        <h2>My Tasks</h2>

        {tasks.length === 0 ? (
          <div className="empty-message">
            No tasks yet.
          </div>
        ) : (
          tasks.map((task) => (
            <div
              className="task-card"
              key={task.id}
            >
              <h3>{task.title}</h3>

              <p>
                <strong>Priority:</strong>{" "}
                {task.priority}
              </p>

              <p>
                <strong>Due date:</strong>{" "}
                {task.due_date || "No due date"}
              </p>

              <div className="task-actions">

                <button
                  className="edit-button"
                  onClick={() => startEditing(task)}
                >
                  Edit
                </button>

                <button
                  className="delete-button"
                  onClick={() => handleDelete(task.id)}
                >
                  Delete
                </button>

              </div>
            </div>
          ))
        )}

      </section>

    </div>
  );
}

export default App;