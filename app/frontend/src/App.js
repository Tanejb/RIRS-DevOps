import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
  const [user, setUser] = useState(null);
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [loginForm, setLoginForm] = useState({ username: '', password: '' });
  const [registerForm, setRegisterForm] = useState({ username: '', password: '' });
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [editingTodo, setEditingTodo] = useState(null);
  const [editForm, setEditForm] = useState({ title: '', description: '' });

  // Set up axios interceptor for auth token
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUserProfile();
      fetchTodos();
    }
  }, []);

  const fetchUserProfile = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/auth/profile`);
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      localStorage.removeItem('token');
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  const fetchTodos = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/todos/`);
      setTodos(response.data.todos);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login`, loginForm);
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      await fetchUserProfile();
      await fetchTodos();
      setLoginForm({ username: '', password: '' });
    } catch (error) {
      alert('Login failed: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post(`${API_BASE_URL}/auth/register`, registerForm);
      alert('Registration successful! Please login.');
      setRegisterForm({ username: '', password: '' });
      setIsLogin(true);
    } catch (error) {
      alert('Registration failed: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    setTodos([]);
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodo.title.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/todos/`, newTodo);
      setTodos([response.data.todo, ...todos]);
      setNewTodo({ title: '', description: '' });
    } catch (error) {
      alert('Error adding todo: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  const handleToggleTodo = async (todoId) => {
    try {
      const response = await axios.patch(`${API_BASE_URL}/todos/${todoId}/toggle`);
      setTodos(todos.map(todo => 
        todo._id === todoId ? response.data.todo : todo
      ));
    } catch (error) {
      alert('Error toggling todo: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleDeleteTodo = async (todoId) => {
    if (!window.confirm('Are you sure you want to delete this todo?')) return;
    
    try {
      await axios.delete(`${API_BASE_URL}/todos/${todoId}`);
      setTodos(todos.filter(todo => todo._id !== todoId));
    } catch (error) {
      alert('Error deleting todo: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleEditTodo = (todo) => {
    setEditingTodo(todo._id);
    setEditForm({ title: todo.title, description: todo.description || '' });
  };

  const handleCancelEdit = () => {
    setEditingTodo(null);
    setEditForm({ title: '', description: '' });
  };

  const handleUpdateTodo = async (todoId) => {
    if (!editForm.title.trim()) {
      alert('Title cannot be empty');
      return;
    }
    
    setLoading(true);
    try {
      const response = await axios.put(`${API_BASE_URL}/todos/${todoId}`, editForm);
      setTodos(todos.map(todo => 
        todo._id === todoId ? response.data.todo : todo
      ));
      setEditingTodo(null);
      setEditForm({ title: '', description: '' });
    } catch (error) {
      alert('Error updating todo: ' + (error.response?.data?.error || error.message));
    }
    setLoading(false);
  };

  if (!user) {
    return (
      <div className="app">
        <div className="auth-container">
          <h1>To-Do App</h1>
          <div className="auth-tabs">
            <button 
              className={isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(true)}
            >
              Login
            </button>
            <button 
              className={!isLogin ? 'active' : ''} 
              onClick={() => setIsLogin(false)}
            >
              Register
            </button>
          </div>
          
          {isLogin ? (
            <form onSubmit={handleLogin} className="auth-form">
              <input
                type="text"
                placeholder="Username"
                value={loginForm.username}
                onChange={(e) => setLoginForm({...loginForm, username: e.target.value})}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister} className="auth-form">
              <input
                type="text"
                placeholder="Username"
                value={registerForm.username}
                onChange={(e) => setRegisterForm({...registerForm, username: e.target.value})}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={registerForm.password}
                onChange={(e) => setRegisterForm({...registerForm, password: e.target.value})}
                required
              />
              <button type="submit" disabled={loading}>
                {loading ? 'Registering...' : 'Register'}
              </button>
            </form>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>To-Do App</h1>
        <div className="user-info">
          <span>Welcome, {user.username}!</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <main className="app-main">
        <form onSubmit={handleAddTodo} className="add-todo-form">
          <input
            type="text"
            placeholder="Add a new todo..."
            value={newTodo.title}
            onChange={(e) => setNewTodo({...newTodo, title: e.target.value})}
            required
          />
          <input
            type="text"
            placeholder="Description (optional)"
            value={newTodo.description}
            onChange={(e) => setNewTodo({...newTodo, description: e.target.value})}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Adding...' : 'Add Todo'}
          </button>
        </form>

        <div className="todos-container">
          <h2>Your Todos ({todos.length})</h2>
          {todos.length === 0 ? (
            <p className="no-todos">No todos yet. Add one above!</p>
          ) : (
            <div className="todos-list">
              {todos.map(todo => (
                <div key={todo._id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                  {editingTodo === todo._id ? (
                    <div className="todo-edit-form">
                      <input
                        type="text"
                        value={editForm.title}
                        onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                        placeholder="Todo title"
                        className="edit-input"
                        required
                      />
                      <input
                        type="text"
                        value={editForm.description}
                        onChange={(e) => setEditForm({...editForm, description: e.target.value})}
                        placeholder="Description (optional)"
                        className="edit-input"
                      />
                      <div className="edit-actions">
                        <button 
                          onClick={() => handleUpdateTodo(todo._id)}
                          className="save-btn"
                          disabled={loading}
                        >
                          {loading ? 'Saving...' : 'Save'}
                        </button>
                        <button 
                          onClick={handleCancelEdit}
                          className="cancel-btn"
                          disabled={loading}
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <>
                  <div className="todo-content">
                    <h3>{todo.title}</h3>
                    {todo.description && <p>{todo.description}</p>}
                    <small>
                      Created: {new Date(todo.created_at).toLocaleDateString()}
                    </small>
                  </div>
                  <div className="todo-actions">
                        <button 
                          onClick={() => handleEditTodo(todo)}
                          className="edit-btn"
                          title="Edit todo"
                        >
                          ✏️
                        </button>
                    <button 
                      onClick={() => handleToggleTodo(todo._id)}
                      className={`toggle-btn ${todo.completed ? 'completed' : ''}`}
                          title={todo.completed ? 'Mark as incomplete' : 'Mark as complete'}
                    >
                      {todo.completed ? '✓' : '○'}
                    </button>
                    <button 
                      onClick={() => handleDeleteTodo(todo._id)}
                      className="delete-btn"
                          title="Delete todo"
                    >
                      🗑️
                    </button>
                  </div>
                    </>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;