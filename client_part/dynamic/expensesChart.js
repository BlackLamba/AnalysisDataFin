// dynamic/expensesChart.js

document.addEventListener("DOMContentLoaded", function () {
  const ctx = document.getElementById("expensesChart").getContext("2d");

  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
      datasets: [
        {
          label: "Расходы (₽)",
          data: [1200, 900, 1500, 800, 1300, 700, 1600],
          backgroundColor: "rgba(248, 113, 113, 0.2)",
          borderColor: "#f87171",
          borderWidth: 2,
          tension: 0.3,
          pointBackgroundColor: "#f87171"
        },
        {
          label: "Доходы",
          data: [5000, 7000, 6000, 8000, 9000, 7500, 8200],
          borderColor: "#60a5fa",
          backgroundColor: "rgba(96, 165, 250, 0.2)",
          tension: 0.3,
          pointBackgroundColor: "#60a5fa"
        },
      ],
    },
    options: {
      plugins: {
        legend: {
          labels: { color: "#f0f0f0" }
        }
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
});
