class TaskManager {
    constructor() {
        this.API_BASE_URL = 'http://localhost:8000/api/tasks';
        this.currentTaskId = null;
        this.isEditMode = false;
        this.initElements();
        this.initEventListeners();
        this.initDarkMode();
        this.loadTasks();
    }

    initElements() {
        // Main elements
        this.tasksList = document.getElementById('tasks-list');
        this.loadingState = document.getElementById('loading-state');
        this.emptyState = document.getElementById('empty-state');
        this.addFirstTaskBtn = document.getElementById('add-first-task');

        // Modal elements
        this.modal = document.getElementById('task-modal');
        this.modalTitle = document.querySelector('.modal-title');
        this.taskForm = document.getElementById('task-form');
        this.taskIdInput = document.getElementById('task-id');
        this.taskNameInput = document.getElementById('task-name');
        this.taskDescInput = document.getElementById('task-description');
        this.taskPomodorosInput = document.getElementById('task-pomodoros');
        this.taskCategoryInput = document.getElementById('task-category');
        this.submitTaskBtn = document.getElementById('submit-task');
        this.submitTaskSpinner = this.submitTaskBtn.querySelector('.spinner');
        this.submitTaskText = this.submitTaskBtn.querySelector('.btn-text');

        // Buttons
        this.addTaskBtn = document.getElementById('add-task-btn');
        this.darkModeToggle = document.getElementById('dark-mode-toggle');
        this.closeModalBtn = document.getElementById('close-modal');
        this.cancelTaskBtn = document.getElementById('cancel-task');
    }

    initEventListeners() {
        // Task actions
        this.addTaskBtn.addEventListener('click', () => this.openModal());
        this.addFirstTaskBtn.addEventListener('click', () => this.openModal());

        // Modal actions
        this.closeModalBtn.addEventListener('click', () => this.closeModal());
        this.cancelTaskBtn.addEventListener('click', () => this.closeModal());
        this.taskForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.isEditMode ? this.updateTask() : this.submitTask();
        });

        // Dark mode toggle
        this.darkModeToggle.addEventListener('click', () => this.toggleDarkMode());

        // Close modal when clicking outside
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.closeModal();
            }
        });
    }

    initDarkMode() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const storedMode = localStorage.getItem('darkMode');

        if (storedMode === 'true' || (prefersDark && storedMode === null)) {
            document.body.classList.add('dark-mode');
            this.darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
    }

    toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);

        this.darkModeToggle.innerHTML = isDarkMode
            ? '<i class="fas fa-sun"></i>'
            : '<i class="fas fa-moon"></i>';
    }

    async loadTasks() {
        try {
            this.showLoadingState();

            const response = await fetch(this.API_BASE_URL);

            if (!response.ok) {
                throw new Error('Failed to fetch tasks');
            }

            const tasks = await response.json();

            if (tasks.length === 0) {
                this.showEmptyState();
            } else {
                this.renderTasks(tasks);
            }
        } catch (error) {
            this.showNotification(error.message, 'error');
            console.error('Error loading tasks:', error);
            this.showEmptyState();
        } finally {
            this.hideLoadingState();
        }
    }

    showLoadingState() {
        this.loadingState.classList.remove('hidden');
        this.emptyState.classList.add('hidden');
        this.tasksList.innerHTML = '';
    }

    hideLoadingState() {
        this.loadingState.classList.add('hidden');
    }

    showEmptyState() {
        this.emptyState.classList.remove('hidden');
        this.tasksList.innerHTML = '';
    }

    renderTasks(tasks) {
        this.emptyState.classList.add('hidden');
        this.tasksList.innerHTML = '';

        tasks.forEach(task => {
            const taskCard = document.createElement('div');
            taskCard.className = 'task-card';
            taskCard.innerHTML = `
                <h3 class="task-title">${task.name}</h3>
                <p class="task-description">${task.description || '<em>No description</em>'}</p>
                <div class="task-meta">
                    <span><i class="fas fa-clock"></i> Pomodoros: ${task.pomodoro_count}</span>
                    <span><i class="fas fa-tag"></i> Category: ${this.getCategoryName(task.category_id)}</span>
                </div>
                <div class="task-date">
                    <small>Created: ${new Date(task.created_at).toLocaleString()}</small>
                </div>
                <div class="task-actions">
                    <button class="btn btn-outline edit-task" data-task-id="${task.id}">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn btn-danger delete-task" data-task-id="${task.id}">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            `;

            taskCard.querySelector('.delete-task').addEventListener('click', () => {
                this.deleteTask(task.id);
            });

            taskCard.querySelector('.edit-task').addEventListener('click', () => {
                this.openModalForEdit(task);
            });

            this.tasksList.appendChild(taskCard);
        });
    }

    getCategoryName(categoryId) {
        const categories = {
            1: 'Work',
            2: 'Personal',
            3: 'Study',
            4: 'Other'
        };
        return categories[categoryId] || 'Unknown';
    }

    openModal() {
        this.isEditMode = false;
        this.modalTitle.textContent = 'Add New Task';
        this.submitTaskText.textContent = 'Add Task';
        this.taskForm.reset();
        this.taskIdInput.value = '';
        this.modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        setTimeout(() => {
            this.taskNameInput.focus();
        }, 100);
    }

    openModalForEdit(task) {
        this.isEditMode = true;
        this.currentTaskId = task.id;
        this.modalTitle.textContent = 'Edit Task';
        this.submitTaskText.textContent = 'Update Task';

        this.taskIdInput.value = task.id;
        this.taskNameInput.value = task.name;
        this.taskDescInput.value = task.description || '';
        this.taskPomodorosInput.value = task.pomodoro_count;
        this.taskCategoryInput.value = task.category_id;

        this.modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        setTimeout(() => {
            this.taskNameInput.focus();
        }, 100);
    }

    closeModal() {
        this.modal.classList.remove('show');
        document.body.style.overflow = 'auto';
        this.currentTaskId = null;
        this.isEditMode = false;
    }

    async submitTask() {
        const name = this.taskNameInput.value.trim();
        const description = this.taskDescInput.value.trim();
        const pomodoros = this.taskPomodorosInput.value;
        const category = this.taskCategoryInput.value;

        if (!name || !pomodoros || !category) {
            this.showNotification('Please fill all required fields', 'error');
            return;
        }

        try {
            this.setSubmitButtonLoading(true);

            const taskData = {
                name,
                description: description || null,
                pomodoro_count: parseInt(pomodoros),
                category_id: parseInt(category)
            };

            const response = await fetch(this.API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to add task');
            }

            const newTask = await response.json();
            this.showNotification('Task added successfully', 'success');
            this.closeModal();
            await this.loadTasks();
        } catch (error) {
            this.showNotification(error.message, 'error');
            console.error('Error adding task:', error);
        } finally {
            this.setSubmitButtonLoading(false);
        }
    }

    async updateTask() {
        const name = this.taskNameInput.value.trim();
        const description = this.taskDescInput.value.trim();
        const pomodoros = this.taskPomodorosInput.value;
        const category = this.taskCategoryInput.value;

        if (!name || !pomodoros || !category) {
            this.showNotification('Please fill all required fields', 'error');
            return;
        }

        try {
            this.setSubmitButtonLoading(true);

            const taskData = {
                name,
                description: description || null,
                pomodoro_count: parseInt(pomodoros),
                category_id: parseInt(category)
            };

            const response = await fetch(`${this.API_BASE_URL}/${this.currentTaskId}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(taskData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to update task');
            }

            const updatedTask = await response.json();
            this.showNotification('Task updated successfully', 'success');
            this.closeModal();
            await this.loadTasks();
        } catch (error) {
            this.showNotification(error.message, 'error');
            console.error('Error updating task:', error);
        } finally {
            this.setSubmitButtonLoading(false);
        }
    }

    setSubmitButtonLoading(isLoading) {
        if (isLoading) {
            this.submitTaskSpinner.classList.remove('hidden');
            this.submitTaskText.classList.add('hidden');
            this.submitTaskBtn.disabled = true;
        } else {
            this.submitTaskSpinner.classList.add('hidden');
            this.submitTaskText.classList.remove('hidden');
            this.submitTaskBtn.disabled = false;
        }
    }

    async deleteTask(taskId) {
        if (!confirm('Are you sure you want to delete this task?')) {
            return;
        }

        try {
            const deleteBtn = document.querySelector(`[data-task-id="${taskId}"]`);
            if (deleteBtn) {
                deleteBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';
                deleteBtn.disabled = true;
            }

            const response = await fetch(`${this.API_BASE_URL}/${taskId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Failed to delete task');
            }

            this.showNotification('Task deleted successfully', 'success');
            await this.loadTasks();
        } catch (error) {
            this.showNotification(error.message, 'error');
            console.error('Error deleting task:', error);
        }
    }

    showNotification(message, type = 'success') {
        const notificationContainer = document.getElementById('notification-container');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.setAttribute('aria-live', 'assertive');

        const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
        notification.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
        `;

        notificationContainer.appendChild(notification);

        // Show notification
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        // Hide after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TaskManager();
});
