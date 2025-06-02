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
    labels: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн'],
    datasets: [
      {
        label: 'Доходы',
        data: [50000, 52000, 48000, 53000, 55000, 57000],
        backgroundColor: 'rgba(96, 165, 250, 0.7)',  // Цвет как в линейной (голубой с прозрачностью)
        borderColor: '#60a5fa',
        borderWidth: 1,
      },
      {
        label: 'Расходы',
        data: [20000, 21000, 19000, 22000, 21000, 23000],
        backgroundColor: 'rgba(248, 113, 113, 0.7)', // Красный с прозрачностью
        borderColor: '#f87171',
        borderWidth: 1,
      },
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        labels: { color: "#f0f0f0" } // цвет легенды
      }
    },
    scales: {
      x: {
        ticks: { color: "#9ca3af" }, // цвет подписей по X
        grid: { color: "#2a2a2a" },  // цвет сетки по X
      },
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 5000,
          color: "#9ca3af",
          callback: function(value) {
            return '₽' + value;
          }
        },
        grid: { color: "#2a2a2a" } // цвет сетки по Y
      }
    }
  }
});

// Столбчатая категорий
const categories = ["Еда", "Транспорт", "Жильё", "Развлечения", "Прочее"];
const data = [2500, 1200, 4000, 1800, 1500];
const colors = ["#34d399", "#60a5fa", "#f87171", "#facc15", "#a78bfa"];

const datasets = categories.map((cat, i) => ({
  label: cat,
  data: data.map((_, idx) => (idx === i ? data[i] : 0)), // показываем только значение для этого датасета
  backgroundColor: colors[i],
  borderWidth: 1,
}));

const barCtx = document.getElementById("categoryBarChart").getContext("2d");
new Chart(barCtx, {
  type: "bar",
  data: {
    labels: ["Еда", "Транспорт", "Жильё", "Развлечения", "Прочее"],
    datasets: [
      {
        label: "Расходы по категориям",
        data: [2500, 1200, 4000, 1800, 1500],
        backgroundColor: [
          "#34d399",
          "#60a5fa",
          "#f87171",
          "#facc15",
          "#a78bfa"
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    indexAxis: 'y', // вот это переключает оси: категории по Y, значения по X
    responsive: true,
    scales: {
      x: {
        beginAtZero: true,
        ticks: {
          callback: value => '₽' + value
        }
      },
      y: {
        ticks: {
          color: "#f0f0f0"
        }
      }
    },
    plugins: {
      legend: {
        labels: { color: "#f0f0f0" },
      },
    },
  },
});


