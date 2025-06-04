async function fetchCurrentMonthStats() {
  const now = new Date();
  const dateParam = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-01`;
  const period = 'month';
  const token = localStorage.getItem('access_token');

  const res = await fetch(`/api/v1/transactions/stats/${period}?date=${dateParam}`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!res.ok) {
    console.error('Ошибка при загрузке данных', await res.json());
    return;
  }

  const data = await res.json();

  const daysInMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
  const labels = Array.from({ length: daysInMonth }, (_, i) => (i + 1).toString());
  const incomeData = Array(daysInMonth).fill(0);
  const expenseData = Array(daysInMonth).fill(0);

  data.data.forEach(item => {
    const dayIndex = new Date(item.transaction_period).getDate() - 1;
    if (dayIndex >= 0 && dayIndex < daysInMonth) {
      if (item.category_type === 'INCOME') {
        incomeData[dayIndex] += item.total_amount;
      } else if (item.category_type === 'EXPENSE') {
        expenseData[dayIndex] += item.total_amount;
      }
    }
  });

  const totalIncome = incomeData.reduce((acc, val) => acc + val, 0);
  const totalExpense = expenseData.reduce((acc, val) => acc + val, 0);

  let profitabilityText = '–';
  let profitabilityColor = 'black';

  if (totalExpense > 0) {
    const profitability = ((totalIncome - totalExpense) / totalExpense) * 100;
    profitabilityText = profitability.toFixed(2) + '%';

    // Вычисляем цвет от красного к зелёному
    const maxPercent = 200; // 200% будет насыщенно зелёный
    const clamped = Math.min(Math.max(profitability, -100), maxPercent);
    const ratio = (clamped + 100) / (maxPercent + 100); // от 0 до 1
    const red = Math.round(255 * (1 - ratio));
    const green = Math.round(255 * ratio);
    profitabilityColor = `rgb(${red}, ${green}, 0)`;
  } else if (totalIncome > 0) {
    profitabilityText = '∞';
    profitabilityColor = 'green';
  }

  // Обновление DOM
  document.querySelector('.card.income p').textContent = `₽ ${totalIncome.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}`;
  document.querySelector('.card.expenses p').textContent = `₽ ${totalExpense.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}`;

  const profitabilityElem = document.getElementById('profitability');
  if (profitabilityElem) {
    profitabilityElem.textContent = profitabilityText;
    profitabilityElem.style.color = profitabilityColor;
  }

  renderChart(
    labels,
    incomeData,
    expenseData,
    data.period || `Месяц: ${now.toLocaleString('ru-RU', { month: 'long', year: 'numeric' })}`
  );
  renderHistogramChart(labels, incomeData, expenseData);
}

function renderChart(labels, incomeData, expenseData, periodLabel) {
  const canvas = document.getElementById('expensesChart');
  if (!canvas) {
    console.error("Элемент #expensesChart не найден в DOM");
    return;
  }

  const ctx = canvas.getContext('2d');
  if (window.myChartInstance) {
    window.myChartInstance.destroy();
  }

  window.myChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Доходы',
          borderColor: 'rgba(54, 162, 235, 0.8)',
          backgroundColor: 'rgba(54, 162, 235, 0.3)',
          data: incomeData,
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Расходы',
          borderColor: 'rgba(255, 99, 132, 0.8)',
          backgroundColor: 'rgba(255, 99, 132, 0.3)',
          data: expenseData,
          fill: false,
          tension: 0.3,
          pointRadius: 4,
          pointHoverRadius: 6,
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `Статистика за период: ${periodLabel}`
        },
        tooltip: {
          mode: 'index',
          intersect: false,
        },
        legend: {
          display: true,
          position: 'top',
        }
      },
      interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function renderHistogramChart(labels, incomeData, expenseData) {
  const ctx = document.getElementById('histogramChart')?.getContext('2d');
  if (!ctx) return;

  if (window.histogramChartInstance) {
    window.histogramChartInstance.destroy();
  }

  window.histogramChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Доходы',
          data: incomeData,
          backgroundColor: 'rgba(75, 192, 192, 0.6)'
        },
        {
          label: 'Расходы',
          data: expenseData,
          backgroundColor: 'rgba(255, 99, 132, 0.6)'
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Гистограмма доходов и расходов и доходов'
        },
        tooltip: {
          mode: 'index',
          intersect: false
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Сумма (₽)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'День месяца'
          }
        }
      }
    }
  });
}


async function fetchCurrentMonthReport() {
  const now = new Date();
  const dateParam = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-01`;
  const token = localStorage.getItem('access_token');
  const period = 'month';

  const res = await fetch(`/api/v1/transactions/report/${period}?date=${dateParam}`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  });

  if (!res.ok) {
    console.error('Ошибка при загрузке отчёта', await res.json());
    return;
  }

  const reportData = await res.json();
  if (!reportData?.data?.[0]) return;

  const report = reportData.data[0];
  const format = val => val != null ? `₽ ${val.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}` : '–';

  document.getElementById('avgIncome').textContent = format(report.average_income);
  document.getElementById('avgExpense').textContent = format(report.average_expense);
  document.getElementById('medianIncome').textContent = format(report.median_income);
  document.getElementById('medianExpense').textContent = format(report.median_expense);
  document.getElementById('modeIncome').textContent = format(report.mode_income);
  document.getElementById('modeExpense').textContent = format(report.mode_expense);
}

// Запуск функций при загрузке
fetchCurrentMonthStats();
fetchCurrentMonthReport();