// Полезные функции для статистики
function standardDeviation(arr) {
  const n = arr.length;
  if (n === 0) return 0;
  const mean = arr.reduce((a, b) => a + b, 0) / n;
  const variance = arr.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
  return Math.sqrt(variance);
}

function coefficientOfVariation(arr) {
  const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
  return mean === 0 ? 0 : (standardDeviation(arr) / mean) * 100;
}

function cumulativeSum(arr) {
  return arr.reduce((acc, val) => acc + val, 0);
}

function buildGroupedIntervals(data, step = 10000) {
  const grouped = new Map();

  data.forEach(value => {
    if (value <= 0) return; // пропускаем нули и отрицательные
    const intervalMin = Math.floor(value / step) * step;
    const intervalMax = intervalMin + step;
    const key = `${intervalMin}-${intervalMax}`;

    if (!grouped.has(key)) {
      grouped.set(key, { min: intervalMin, max: intervalMax, freq: 0 });
    }
    grouped.get(key).freq += 1;
  });

  // Сортировка по min
  return Array.from(grouped.values()).sort((a, b) => a.min - b.min);
}

function medianGrouped(intervals) {
  const total = intervals.reduce((sum, i) => sum + i.freq, 0);
  const half = total / 2;

  let cumulative = 0;
  let medianInterval = null;
  let F = 0;

  for (let i = 0; i < intervals.length; i++) {
    const curr = intervals[i];
    if (cumulative + curr.freq >= half) {
      medianInterval = curr;
      F = cumulative;
      break;
    }
    cumulative += curr.freq;
  }

  if (!medianInterval) return null;

  const { min: L, max, freq: f } = medianInterval;
  const h = max - L;

  return L + ((half - F) / f) * h;
}

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
  const labels = Array.from({ length: daysInMonth }, (_, i) => {
      const day = new Date(now.getFullYear(), now.getMonth(), i + 1);
      return day.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }); // например: 01.06.2025
  });
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

  // Вычисляем min/max
  const maxIncome = Math.max(...incomeData);
  const minIncome = Math.min(...incomeData.filter(v => v > 0));
  const maxExpense = Math.max(...expenseData);
  const minExpense = Math.min(...expenseData.filter(v => v > 0));

  // Форматирование
  const format = val =>
    val != null && isFinite(val)
      ? `₽ ${val.toLocaleString('ru-RU', { minimumFractionDigits: 2 })}`
      : '–';

  // Обновляем DOM
  document.getElementById('maxIncome').textContent = format(maxIncome);
  document.getElementById('minIncome').textContent = format(minIncome);
  document.getElementById('maxExpense').textContent = format(maxExpense);
  document.getElementById('minExpense').textContent = format(minExpense);

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


  // Дополнительные статистики
  document.getElementById('stdIncome').textContent = standardDeviation(incomeData).toFixed(2);
  document.getElementById('stdExpense').textContent = standardDeviation(expenseData).toFixed(2);
  const cvIncomeValue = coefficientOfVariation(incomeData);
  const cvExpenseValue = coefficientOfVariation(expenseData);

  const cvIncomeElem = document.getElementById('cvIncome');
  const cvExpenseElem = document.getElementById('cvExpense');

  const cvThreshold = 30; // порог для красного цвета

  cvIncomeElem.textContent = cvIncomeValue.toFixed(2) + '%';
  cvExpenseElem.textContent = cvExpenseValue.toFixed(2) + '%';

  cvIncomeElem.style.color = cvIncomeValue > cvThreshold ? 'red' : 'black';
  cvExpenseElem.style.color = cvExpenseValue > cvThreshold ? 'red' : 'black';

  const groupedIncome = buildGroupedIntervals(incomeData, 10000);
  const groupedExpense = buildGroupedIntervals(expenseData, 10000);

  const medianIncomeGrouped = medianGrouped(groupedIncome);
  const medianExpenseGrouped = medianGrouped(groupedExpense);

  document.getElementById('groupedMedianIncome').textContent =
    isNaN(medianIncomeGrouped) ? '–' : `₽ ${medianIncomeGrouped.toFixed(2)}`;

  document.getElementById('groupedMedianExpense').textContent =
    isNaN(medianExpenseGrouped) ? '–' : `₽ ${medianExpenseGrouped.toFixed(2)}`;
  console.table(groupedIncome);

  document.getElementById('countIncome').textContent = countNonZero(incomeData);
  document.getElementById('countExpense').textContent = countNonZero(expenseData);
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
          pointRadius: 3,
          pointHoverRadius: 4,
          pointBackgroundColor: "#60a5fa"
        },
        {
          label: 'Расходы',
          borderColor: 'rgba(255, 99, 132, 0.8)',
          backgroundColor: 'rgba(255, 99, 132, 0.3)',
          data: expenseData,
          fill: false,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 4,
          pointBackgroundColor: "#f87171"
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `Линейный график доходов и расходов`
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
          backgroundColor: 'rgba(54, 162, 235, 0.3)',
          borderColor: 'rgba(54, 162, 235, 0.8)',
          borderWidth: 1,
          borderRadius: 4,
          barPercentage: 1,
          categoryPercentage: 1
        },
        {
          label: 'Расходы',
          data: expenseData,
          backgroundColor: 'rgba(255, 99, 132, 0.3)',
          borderColor: 'rgba(255, 99, 132, 0.8)',
          borderWidth: 1,
          borderRadius: 4,
          barPercentage: 1,
          categoryPercentage: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: 'Гистограмма доходов и расходов'
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
window.addEventListener('DOMContentLoaded', () => {
  fetchCurrentMonthStats();
  fetchCurrentMonthReport();
});