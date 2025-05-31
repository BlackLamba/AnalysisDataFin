document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const errorMsg = document.getElementById('error-msg');

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Ошибка авторизации');
      }

      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);

      window.location.href = './dashboard.html';
    } catch (err) {
      errorMsg.textContent = err.message;
    }
  });
});
