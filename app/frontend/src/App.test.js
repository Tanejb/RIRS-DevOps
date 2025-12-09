import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import App from './App';

jest.mock('axios');

const profileResponse = {
  data: { username: 'testuser', created_at: new Date().toISOString() },
};

const todosResponse = {
  data: {
    todos: [
      {
        _id: '1',
        title: 'First todo',
        description: 'desc',
        completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ],
  },
};

beforeEach(() => {
  jest.clearAllMocks();
  localStorage.clear();
  delete axios.defaults.headers.common['Authorization'];
});

test('shows login form by default', () => {
  render(<App />);
  const loginButtons = screen.getAllByText(/login/i);
  expect(loginButtons.length).toBeGreaterThanOrEqual(2); // tab + submit
  expect(screen.getByPlaceholderText(/username/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
});

test('switches to register tab', () => {
  render(<App />);
  fireEvent.click(screen.getByText(/register/i));
  const registerButtons = screen.getAllByText(/register/i);
  expect(registerButtons.length).toBeGreaterThanOrEqual(2); // tab + submit
});

test('loads profile and todos when token exists', async () => {
  localStorage.setItem('token', 'abc');
  axios.get.mockResolvedValueOnce(profileResponse).mockResolvedValueOnce(todosResponse);

  render(<App />);

  await waitFor(() => expect(screen.getByText(/welcome, testuser/i)).toBeInTheDocument());
  expect(screen.getByText(/Your Todos \(1\)/i)).toBeInTheDocument();
});

test('successful login stores token and loads data', async () => {
  axios.post.mockResolvedValueOnce({
    data: { access_token: 'tok123', user: { username: 'loginuser' } },
  });
  axios.get.mockResolvedValueOnce(profileResponse).mockResolvedValueOnce(todosResponse);

  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/username/i), { target: { value: 'u' } });
  fireEvent.change(screen.getByPlaceholderText(/password/i), { target: { value: 'p' } });
  fireEvent.click(screen.getAllByText(/login/i)[1]); // submit button

  await waitFor(() => expect(screen.getByText(/welcome, testuser/i)).toBeInTheDocument());
  expect(localStorage.getItem('token')).toBe('tok123');
});

test('adds a todo and prepends to the list', async () => {
  localStorage.setItem('token', 'abc');
  axios.get.mockResolvedValueOnce(profileResponse).mockResolvedValueOnce({
    data: { todos: [] },
  });

  axios.post.mockResolvedValueOnce({
    data: {
      todo: {
        _id: '2',
        title: 'New todo',
        description: '',
        completed: false,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    },
  });

  render(<App />);

  await waitFor(() => expect(screen.getByText(/your todos/i)).toBeInTheDocument());

  fireEvent.change(screen.getByPlaceholderText(/add a new todo/i), {
    target: { value: 'New todo' },
  });
  fireEvent.click(screen.getByText(/add todo/i));

  await waitFor(() => expect(screen.getByText('New todo')).toBeInTheDocument());
});

test('toggles a todo', async () => {
  localStorage.setItem('token', 'abc');
  axios.get.mockResolvedValueOnce(profileResponse).mockResolvedValueOnce(todosResponse);
  axios.patch.mockResolvedValueOnce({
    data: {
      todo: { ...todosResponse.data.todos[0], completed: true },
    },
  });

  render(<App />);
  await waitFor(() => expect(screen.getByText(/first todo/i)).toBeInTheDocument());

  fireEvent.click(screen.getByTitle(/mark as complete/i));

  await waitFor(() => expect(screen.getByText('✓')).toBeInTheDocument());
});

test('deletes a todo', async () => {
  localStorage.setItem('token', 'abc');
  axios.get.mockResolvedValueOnce(profileResponse).mockResolvedValueOnce(todosResponse);
  axios.delete.mockResolvedValueOnce({});
  window.confirm = jest.fn(() => true);

  render(<App />);
  await waitFor(() => expect(screen.getByText(/first todo/i)).toBeInTheDocument());

  fireEvent.click(screen.getByTitle(/delete todo/i));

  await waitFor(() => expect(screen.queryByText(/first todo/i)).not.toBeInTheDocument());
});

test('logout clears user and todos', async () => {
  localStorage.setItem('token', 'abc');
  axios.get.mockResolvedValueOnce(profileResponse).mockResolvedValueOnce(todosResponse);

  render(<App />);
  await waitFor(() => expect(screen.getByText(/welcome, testuser/i)).toBeInTheDocument());

  fireEvent.click(screen.getByText(/logout/i));

  await waitFor(() => expect(screen.getAllByText(/login/i).length).toBeGreaterThanOrEqual(1));
  expect(localStorage.getItem('token')).toBeNull();
});
