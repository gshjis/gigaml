import { tasksApi } from './api.js';

document.addEventListener('DOMContentLoaded', async () => {
  const tasksContainer = document.getElementById('tasks-container');
  const taskForm = document.getElementById('task-form');
  const logoutBtn = document.getElementById('logout-btn');

  // Загрузка задач
  async function loadTasks() {
    try {
      const tasks = await tasksApi.getAll();
      renderTasks(tasks);
    } catch (error) {
      alert(`Failed to load tasks: ${error.message}`);
    }
  }

  // Рендер задач
  function renderTasks(tasks) {
    tasksContainer.innerHTML = tasks.map(task => `
      <div class="task-card" data-id="${task.id}">
        <h3>${task.name}</h3>
        <p>Pomodoros: ${task.pomodoro_count}</p>
        <div class="task-actions">
          <button class="edit-btn">✏️</button>
          <button class="delete-btn">🗑️</button>
        </div>
      </div>
    `).join('');

    // Добавляем обработчики
    document.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', handleDelete);
    });

    document.querySelectorAll('.edit-btn').forEach(btn => {
      btn.addEventListener('click', handleEdit);
    });
  }

  // Создание задачи
  taskForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(taskForm);
    const taskData = {
      name: formData.get('name'),
      pomodoro_count: parseInt(formData.get('pomodoro_count')),
      category_id: parseInt(formData.get('category_id'))
    };

    try {
      await tasksApi.create(taskData);
      taskForm.reset();
      await loadTasks();
    } catch (error) {
      alert(`Failed to create task: ${error.message}`);
    }
  });

  // Удаление задачи
  async function handleDelete(e) {
    const taskId = e.target.closest('.task-card').dataset.id;
    
    if (confirm('Delete this task?')) {
      try {
        await tasksApi.delete(taskId);
        await loadTasks();
      } catch (error) {
        alert(`Failed to delete task: ${error.message}`);
      }
    }
  }

  // Редактирование задачи
  function handleEdit(e) {
    const taskCard = e.target.closest('.task-card');
    const taskId = taskCard.dataset.id;
    
    // Реализуем модальное окно или inline-редактирование
    alert(`Edit task ${taskId} - implement modal here`);
  }

  // Выход
  logoutBtn.addEventListener('click', () => {
    // Очищаем куки (нужно добавить logout endpoint в API)
    document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'refresh_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/login.html';
  });

  // Инициализация
  await loadTasks();
});