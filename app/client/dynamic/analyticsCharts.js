document.addEventListener("DOMContentLoaded", () => {
  const today = new Date().toISOString().split("T")[0];
  const dateInput = document.querySelector("input[type='date']");

  if (dateInput) {
    dateInput.value = today;
  }

  fetchAndRenderAnalytics(today, "month", "");

  document.querySelector(".filter-form")?.addEventListener("submit", function (e) {
    e.preventDefault();

    const dateInput = this.querySelector("input[type='date']");
    const periodSelect = this.querySelector("select[name='period']");
    const typeSelect = this.querySelector("select[name='type']");

    if (!dateInput || !periodSelect || !typeSelect) {
      console.error("Не удалось найти один из элементов формы.");
      return;
    }

    const today = new Date().toISOString().split("T")[0];
    const date = dateInput.value || today;
    const period = periodSelect.value;
    const type = typeSelect.value;

    fetchAndRenderAnalytics(date, period, type);
  });
});

async function fetchAndRenderAnalytics(date, period, type) {
  const token = localStorage.getItem("access_token");
  type = type || "EXPENSE";

  if (!date) {
    console.error("Необходимо указать дату");
    return;
  }

  try {
    const overviewUrl = `/api/v1/transactions/stats/${period}?date=${date}&type=${type}`;
    const overviewRes = await fetch(overviewUrl, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    if (!overviewRes.ok) {
      throw new Error(`Ошибка HTTP: ${overviewRes.status}`);
    }
    const overviewRaw = await overviewRes.json();

    const categoriesUrl = `/api/v1/transactions/categories/${type}/${period}?date=${date}`;
    const categoriesRes = await fetch(categoriesUrl, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    if (!categoriesRes.ok) {
      throw new Error(`Ошибка HTTP: ${categoriesRes.status}`);
    }
    const categoryData = await categoriesRes.json();

    let transformedOverviewData = { labels: [], income: [], expense: [] };

    if (period === "day") {
      overviewRaw.data.forEach(item => {
        transformedOverviewData.labels.push(`${item.transaction_period}:00`);
        if (item.category_type === "INCOME") {
          transformedOverviewData.income.push(item.total_amount);
          transformedOverviewData.expense.push(0);
        } else {
          transformedOverviewData.expense.push(item.total_amount);
          transformedOverviewData.income.push(0);
        }
      });
    } else {
      transformedOverviewData = transformStatsData(overviewRaw, period);
    }

    renderLineChart(
      transformedOverviewData.labels,
      transformedOverviewData.income,
      transformedOverviewData.expense
    );
    renderBarChart(transformedOverviewData);
    renderPieChart(categoryData);
    renderCategoryBarChart(categoryData);

  } catch (error) {
    console.error("Ошибка при загрузке аналитики:", error);
    const errorElement = document.getElementById("chart-error");
    if (errorElement) {
      errorElement.textContent = "Не удалось загрузить данные. Пожалуйста, проверьте параметры и попробуйте снова.";
      errorElement.style.display = "block";
    }
  }
}

function transformStatsData(rawData, period) {
  const result = {
    labels: [],
    income: [],
    expense: []
  };

  if (period === "day") {
    rawData.data.forEach(item => {
      const hour = item.transaction_period.padStart(2, "0");
      result.labels.push(`${hour}:00`);

      if (item.category_type === "INCOME") {
        result.income.push(item.total_amount);
        result.expense.push(0);
      } else {
        result.expense.push(item.total_amount);
        result.income.push(0);
      }
    });
  } else {
    rawData.data.forEach(item => {
      result.labels.push(item.transaction_period);

      if (item.category_type === "INCOME") {
        result.income.push(item.total_amount);
        result.expense.push(0);
      } else {
        result.expense.push(item.total_amount);
        result.income.push(0);
      }
    });
  }

  return result;
}

function renderLineChart(labels, income, expense) {
  const ctx = document.getElementById("lineChart").getContext("2d");

  if (window.lineChartInstance) window.lineChartInstance.destroy();

  window.lineChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Доходы",
          data: income,
          borderColor: "#60a5fa",
          backgroundColor: "rgba(96, 165, 250, 0.2)",
          tension: 0.3,
          pointBackgroundColor: "#60a5fa"
        },
        {
          label: "Расходы",
          data: expense,
          borderColor: "#f87171",
          backgroundColor: "rgba(248, 113, 113, 0.2)",
          tension: 0.3,
          pointBackgroundColor: "#f87171"
        }
      ]
    },
    options: {
      plugins: {
        legend: { labels: { color: "#f0f0f0" } }
      },
      scales: {
        x: {
          ticks: { color: "#9ca3af" },
          grid: { color: "#2a2a2a" }
        },
        y: {
          ticks: { color: "#9ca3af" },
          grid: { color: "#2a2a2a" }
        }
      }
    }
  });
}

function renderBarChart(data) {
  const ctx = document.getElementById("incomeExpensesChart").getContext("2d");
  const labels = data.labels || [];
  const income = data.income || [];
  const expense = data.expense || [];

  if (window.barChartInstance) window.barChartInstance.destroy();

  window.barChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Доходы",
          data: income,
          backgroundColor: "rgba(96, 165, 250, 0.7)",
          borderColor: "#60a5fa",
          borderWidth: 1
        },
        {
          label: "Расходы",
          data: expense,
          backgroundColor: "rgba(248, 113, 113, 0.7)",
          borderColor: "#f87171",
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { color: "#f0f0f0" }
        }
      },
      scales: {
        x: {
          ticks: { color: "#9ca3af" },
          grid: { color: "#2a2a2a" }
        },
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 5000,
            color: "#9ca3af",
            callback: value => `₽${value}`
          },
          grid: { color: "#2a2a2a" }
        }
      }
    }
  });
}

function renderPieChart(data) {
  const ctx = document.getElementById("categoryPieChart").getContext("2d");
  const categories = data?.data || [];

  const labels = categories.map(item => item.category_name);
  const values = categories.map(item => item.total_amount);
  const colors = ["#34d399", "#60a5fa", "#f87171", "#facc15", "#a78bfa", "#f472b6", "#818cf8"];

  if (window.pieChartInstance) window.pieChartInstance.destroy();

  window.pieChartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, values.length)
      }]
    },
    options: {
      plugins: {
        legend: { labels: { color: "#f0f0f0" } }
      }
    }
  });
}

function renderCategoryBarChart(data) {
  const ctx = document.getElementById("categoryBarChart").getContext("2d");
  const categories = data?.data || [];

  const labels = categories.map(item => item.category_name);
  const values = categories.map(item => item.total_amount);
  const colors = ["#34d399", "#60a5fa", "#f87171", "#facc15", "#a78bfa", "#f472b6", "#818cf8"];

  if (window.categoryBarChartInstance) window.categoryBarChartInstance.destroy();

  window.categoryBarChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Расходы по категориям",
        data: values,
        backgroundColor: colors.slice(0, values.length),
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      plugins: {
        legend: { labels: { color: "#f0f0f0" } }
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: {
            callback: value => `₽${value}`
          }
        },
        y: {
          ticks: { color: "#f0f0f0" }
        }
      }
    }
  });
}