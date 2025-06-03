document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('transaction-form');
  const amountInput = document.getElementById('amount');
  const typeSelect = document.getElementById('type');
  const dateInput = document.getElementById('date');
  const categorySelect = document.getElementById('category');
  const descriptionInput = document.getElementById('description');

  const token = localStorage.getItem('access_token');
  const userId = localStorage.getItem('user_id');

  if (!token || !userId) {
    alert('Пожалуйста, войдите в систему');
    window.location.href = '/login';
    return;
  }

  // Установка текущей даты
  dateInput.valueAsDate = new Date();

  // При смене типа операции — обновляем категории
  typeSelect.addEventListener('change', async () => {
    if (typeSelect.value) {
      await loadCategories(typeSelect.value);
    } else {
      resetCategorySelect();
    }
  });

  // Отправка формы
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const validationError = validateForm();
    if (validationError) {
      alert(validationError);
      return;
    }

    const transactionData = {
      UserID: userId,
      CategoryID: categorySelect.value,
      Amount: parseFloat(amountInput.value),
      Type: typeSelect.value,
      Description: descriptionInput.value.trim(),
      TransactionDate: new Date(dateInput.value).toISOString()
    };

    try {
      const response = await fetch('/api/v1/transactions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(transactionData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка сервера');
      }

      alert('Операция успешно добавлена!');
      form.reset();
      resetCategorySelect();
      dateInput.valueAsDate = new Date();

    } catch (error) {
      console.error('Ошибка:', error);
      alert(`Ошибка: ${error.message}`);
    }
  });

  async function loadCategories(type) {
    try {
      const response = await fetch(`/api/v1/categories?type=${type}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) throw new Error('Ошибка загрузки категорий');

      const categories = await response.json();
      console.log('Категории с сервера:', categories);  // Для отладки
      updateCategorySelect(categories);

    } catch (error) {
      console.error('Ошибка загрузки категорий:', error);
      alert('Не удалось загрузить категории');
    }
  }

  function updateCategorySelect(categories) {
    const selectedType = typeSelect.value;
    const filtered = categories.filter(c => c.Type === selectedType);

    categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
    filtered.forEach(category => {
      const option = document.createElement('option');
      option.value = category.CategoryID;
      option.textContent = category.Category || 'Без названия';
      categorySelect.appendChild(option);
    });
  }


  function resetCategorySelect() {
    categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
  }

  function validateForm() {
    if (!amountInput.value || parseFloat(amountInput.value) <= 0) {
      return 'Введите корректную сумму';
    }
    if (!typeSelect.value) {
      return 'Выберите тип операции';
    }
    if (!categorySelect.value) {
      return 'Выберите категорию';
    }
    if (!dateInput.value) {
      return 'Укажите дату операции';
    }
    return null;
  }
});