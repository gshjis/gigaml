import { authApi } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  // Обработка входа
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(loginForm);
    const credentials = {
      username: formData.get('email'),
      password: formData.get('password')
    };

    try {
      await authApi.login(credentials);
      window.location.href = '/tasks.html';
    } catch (error) {
      alert(`Login failed: ${error.message}`);
    }
  });

  // Обработка регистрации
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(registerForm);
    const userData = {
      email: formData.get('email'),
      password: formData.get('password'),
      name: formData.get('name')
    };

    try {
      await authApi.register(userData);
      alert('Registration successful! Please login');
      loginForm.reset();
      registerForm.reset();
    } catch (error) {
      alert(`Registration failed: ${error.message}`);
    }
  });
});