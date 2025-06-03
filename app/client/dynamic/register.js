document.addEventListener('DOMContentLoaded', () => {
  const registerForm = document.getElementById('registerForm');
  const errorMsg = document.getElementById('error-msg');

  if (!registerForm) {
    console.error('Форма регистрации не найдена');
    return;
  }

  registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    // Получаем значения полей
    const formData = {
      first_name: document.getElementById('first_name').value.trim(),
      last_name: document.getElementById('last_name').value.trim(),
      father_name: document.getElementById('father_name').value.trim(),
      email: document.getElementById('email').value.trim().toLowerCase(),
      password: document.getElementById('password').value,
      confirmPassword: document.getElementById('confirmPassword').value
    };

    // Валидация
    if (!validateForm(formData)) {
      return;
    }

    try {
      // Показываем индикатор загрузки
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Регистрация...';

      // Отправляем запрос
      const response = await fetch('http://localhost:8000/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          first_name: formData.first_name,
          last_name: formData.last_name,
          father_name: formData.father_name,
          email: formData.email,
          password: formData.password
        }),
      });

      // Обрабатываем ответ
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка регистрации');
      }

      // Успешная регистрация
      showSuccessMessage('Регистрация прошла успешно! Перенаправляем на страницу входа...');

      // Перенаправляем через 2 секунды
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);

    } catch (err) {
      console.error('Ошибка регистрации:', err);
      showErrorMessage(err.message || 'Произошла ошибка при регистрации');
    } finally {
      // Восстанавливаем кнопку
      const submitBtn = registerForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Зарегистрироваться';
      }
    }
  });

  // Функции валидации и отображения сообщений
  function validateForm(formData) {
    // Проверка паролей
    if (formData.password !== formData.confirmPassword) {
      showErrorMessage('Пароли не совпадают');
      return false;
    }

    // Проверка длины пароля
    if (formData.password.length < 8) {
      showErrorMessage('Пароль должен содержать минимум 8 символов');
      return false;
    }

    // Проверка email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      showErrorMessage('Введите корректный email');
      return false;
    }

    // Проверка обязательных полей
    const requiredFields = ['first_name', 'last_name', 'email'];
    for (const field of requiredFields) {
      if (!formData[field]) {
        showErrorMessage(`Поле ${field.replace('_', ' ')} обязательно для заполнения`);
        return false;
      }
    }

    return true;
  }

  function showErrorMessage(message) {
    if (errorMsg) {
      errorMsg.textContent = message;
      errorMsg.style.display = 'block';
      errorMsg.style.color = 'red';
    } else {
      alert(message);
    }
  }

  function showSuccessMessage(message) {
    if (errorMsg) {
      errorMsg.textContent = message;
      errorMsg.style.display = 'block';
      errorMsg.style.color = 'green';
    } else {
      alert(message);
    }
  }
});