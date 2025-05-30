// dynamic/analyticsCharts.js
document.addEventListener("DOMContentLoaded", function () {
  // Линейный график: Доходы и Расходы по дням
  const lineCtx = document.getElementById("lineChart").getContext("2d");
  new Chart(lineCtx, {
    type: "line",
    data: {
      labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      datasets: [
        {
          label: "Доходы",
          data: [5000, 7000, 6000, 8000, 9000, 7500, 8200],
          borderColor: "#60a5fa",
          backgroundColor: "rgba(96, 165, 250, 0.2)",
          tension: 0.3,
          pointBackgroundColor: "#60a5fa"
        },
        {
          label: "Расходы",
          data: [3000, 2500, 4000, 3500, 2000, 3000, 4500],
          borderColor: "#f87171",
          backgroundColor: "rgba(248, 113, 113, 0.2)",
          tension: 0.3,
          pointBackgroundColor: "#f87171"
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          labels: { color: "#f0f0f0" },
        },
      },
      scales: {
        x: {
          ticks: { color: "#9ca3af" },
          grid: { color: "#2a2a2a" },
        },
        y: {
          ticks: { color: "#9ca3af" },
          grid: { color: "#2a2a2a" },
        },
      },
    },
  });

  // Круговая диаграмма: Распределение по категориям
const pieCtx = document.getElementById("pieChart").getContext("2d");
new Chart(pieCtx, {
    type: "pie",
    data: {
      labels: ["Еда", "Транспорт", "Жильё", "Развлечения", "Прочее"],
      datasets: [
        {
          data: [2500, 1200, 4000, 1800, 1500],
          backgroundColor: [
            "#34d399",
            "#60a5fa",
            "#f87171",
            "#facc15",
            "#a78bfa"
          ],
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          labels: { color: "#f0f0f0" },
        },
      },
    },
  });
});

const ctx = document.getElementById('incomeExpensesChart').getContext('2d');

const incomeExpensesChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'], // Месяцы или другие периоды
    datasets: [
      {
        label: 'Доходы',
        data: [50000, 52000, 48000, 53000, 55000, 57000], // сюда динамические данные
        backgroundColor: 'rgba(54, 162, 235, 0.7)', // синий
      },
      {
        label: 'Расходы',
        data: [20000, 21000, 19000, 22000, 21000, 23000],
        backgroundColor: 'rgba(255, 99, 132, 0.7)', // красный
      },
    ]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 5000,
          callback: function(value) {
            return '₽' + value;
          }
        }
      }
    }
  }
});

// Пример данных (замени на свои реальные)
const categories = ['Зарплата', 'Аренда', 'Продукты', 'Развлечения', 'Транспорт'];
const categoryValues = [30000, 15000, 8000, 6000, 2000];
const categoryColors = [
  'rgba(54, 162, 235, 0.7)',
  'rgba(255, 206, 86, 0.7)',
  'rgba(75, 192, 192, 0.7)',
  'rgba(255, 99, 132, 0.7)',
  'rgba(153, 102, 255, 0.7)'
];

// Столбчатая диаграмма с теми же данными
const barCtx = document.getElementById('categoryBarChart').getContext('2d');
const categoryBarChart = new Chart(barCtx, {
  type: 'bar',
  data: {
    labels: categories,
    datasets: [{
      label: 'Сумма по категориям',
      data: categoryValues,
      backgroundColor: categoryColors,
      borderWidth: 1,
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return '₽' + value;
          }
        }
      }
    }
  }
});
