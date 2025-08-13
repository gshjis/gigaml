document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const taskForm = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');
    const logoutButton = document.getElementById('logout');

    if (!token) {
        window.location.href = '/login.html';
        return;
    }

    async function loadTasks() {
        try {
            const response = await fetch('/api/tasks/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const tasks = await response.json();
                taskList.innerHTML = tasks.map(task => `
                    <div class="task">
                        <span>${task.title}</span>
                        <button onclick="deleteTask(${task.id})">Удалить</button>
                    </div>
                `).join('');
            } else {
                const errorData = await response.json();
                alert(errorData.detail || 'Не удалось загрузить задачи');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при загрузке задач');
        }
    }

    window.deleteTask = async (taskId) => {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                await loadTasks();
            } else {
                const errorData = await response.json();
                alert(errorData.detail || 'Не удалось удалить задачу');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при удалении задачи');
        }
    };

    if (taskForm) {
        taskForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = e.target.title.value;

            try {
                const response = await fetch('/api/tasks/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ title })
                });

                if (response.ok) {
                    e.target.title.value = '';
                    await loadTasks();
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Не удалось создать задачу');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при создании задачи');
            }
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.href = '/login.html';
        });
    }

    loadTasks();
});
