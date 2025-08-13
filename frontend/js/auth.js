document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = e.target.email.value;
            const password = e.target.password.value;

            try {
                const response = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('token', data.access_token);
                    window.location.href = '/tasks.html';
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Ошибка входа');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Не удалось выполнить вход');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = e.target.username.value;
            const email = e.target.email.value;
            const password = e.target.password.value;

            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, email, password })
                });

                if (response.ok) {
                    alert('Регистрация успешна');
                    window.location.href = '/login.html';
                } else {
                    const errorData = await response.json();
                    alert(errorData.detail || 'Ошибка регистрации');
                }
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Не удалось зарегистрироваться');
            }
        });
    }
});
