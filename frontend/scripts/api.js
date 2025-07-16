const API_BASE = 'http://backend:8000'; // Для прода: заменить на домен

async function apiFetch(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include' // Для кук
  };

  if (body) options.body = JSON.stringify(body);

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  
  if (response.status === 401) {
    // Перенаправление на логин при истечении сессии
    window.location.href = '/login.html';
    return;
  }

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API error');
  }

  return response.json();
}

// Auth API
export const authApi = {
  register: (userData) => apiFetch('/auth/register', 'POST', userData),
  login: (credentials) => apiFetch('/auth/login', 'POST', credentials),
};

// Tasks API
export const tasksApi = {
  getAll: () => apiFetch('/api/tasks'),
  create: (taskData) => apiFetch('/api/tasks', 'POST', taskData),
  update: (id, taskData) => apiFetch(`/api/tasks/${id}`, 'PATCH', taskData),
  delete: (id) => apiFetch(`/api/tasks/${id}`, 'DELETE'),
};