import React, { useState, useEffect } from 'react';
import './App.css';

interface Task {
  id: number;
  title: string;
  completed: boolean;
  created_at: string;
}

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState('');
  const [loading, setLoading] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${API_URL}/api/tasks`);
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTask }),
      });
      const task = await response.json();
      setTasks([...tasks, task]);
      setNewTask('');
    } catch (error) {
      console.error('Error adding task:', error);
    }
    setLoading(false);
  };

  const toggleTask = async (id: number) => {
    try {
      const task = tasks.find(t => t.id === id);
      const response = await fetch(`${API_URL}/api/tasks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !task?.completed }),
      });
      const updatedTask = await response.json();
      setTasks(tasks.map(t => t.id === id ? updatedTask : t));
    } catch (error) {
      console.error('Error updating task:', error);
    }
  };

  const deleteTask = async (id: number) => {
    try {
      await fetch(`${API_URL}/api/tasks/${id}`, { method: 'DELETE' });
      setTasks(tasks.filter(t => t.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>📝 TaskFlow - Simple Task Manager</h1>

        <form onSubmit={addTask} className="task-form">
          <input
            type="text"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
            placeholder="What needs to be done?"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Adding...' : 'Add Task'}
          </button>
        </form>

        <div className="tasks-list">
          {tasks.length === 0 ? (
            <p className="empty-state">No tasks yet. Add one above!</p>
          ) : (
            tasks.map(task => (
              <div key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleTask(task.id)}
                />
                <span className="task-title">{task.title}</span>
                <button onClick={() => deleteTask(task.id)} className="delete-btn">
                  Delete
                </button>
              </div>
            ))
          )}
        </div>

        <div className="footer">
          <p>{tasks.filter(t => !t.completed).length} tasks remaining</p>
        </div>
      </div>
    </div>
  );
}

export default App;
