document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('loginForm');
  const errorMsg = document.getElementById('error-msg');

  /**
   * Парсинг JWT токена
   * @param {string} token - JWT токен
   * @returns {object|null} Распарсенный payload или null при ошибке
   */
  function parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      console.error('JWT parsing error:', e);
      return null;
    }
  }

  /**
   * Сохраняет данные аутентификации
   * @param {string} accessToken - JWT токен доступа
   * @param {object} payload - Распарсенный payload токена
   */
  function saveAuthData(accessToken, payload) {
    if (!payload) {
      throw new Error('Invalid token payload');
    }

    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('user_id', payload.user_id || '');
    localStorage.setItem('email', payload.sub || '');

    console.log('Auth data saved:', {
      access_token: accessToken,
      user_id: payload.user_id,
      email: payload.sub
    });
  }

  /**
   * Обработка успешной аутентификации
   */
  function handleAuthSuccess() {
    // Перенаправляем на главную страницу или обновляем интерфейс
    window.location.href = '/';
  }

  /**
   * Обработка ошибки аутентификации
   * @param {string} message - Сообщение об ошибке
   */
  function handleAuthError(message) {
    console.error('Authentication error:', message);
    if (errorMsg) {
      errorMsg.textContent = message;
      errorMsg.style.display = 'block';
    }
  }

  /**
   * Обработчик отправки формы
   * @param {Event} e - Событие формы
   */
  async function handleSubmit(e) {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    try {
      // Отправляем запрос на сервер
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      // Обрабатываем ответ
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка авторизации');
      }

      const data = await response.json();
      console.log('API response:', data);

      // Парсим токен
      const payload = parseJwt(data.access_token);
      if (!payload) {
        throw new Error('Неверный формат токена');
      }

      // Сохраняем данные
      saveAuthData(data.access_token, payload);

      // Перенаправляем пользователя
      handleAuthSuccess();

    } catch (err) {
      handleAuthError(err.message);
    }
  }

  // Добавляем обработчик формы, если она существует
  if (form) {
    form.addEventListener('submit', handleSubmit);
  } else {
    console.warn('Login form not found');
  }

  // Проверяем, есть ли уже токен при загрузке страницы
  const token = localStorage.getItem('access_token');
  if (token) {
    console.log('Found existing token, payload:', parseJwt(token));
  }
});