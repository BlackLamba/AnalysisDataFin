document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;
  const navItems = document.querySelectorAll(".sidebar li");

  navItems.forEach((li) => {
    if (path.includes("dashboard") && li.textContent.includes("Сводка")) {
      li.classList.add("active");
    } else if (path.includes("analytics") && li.textContent.includes("Аналитика")) {
      li.classList.add("active");
    } else if (path.includes("input") && li.textContent.includes("Операции")) {
      li.classList.add("active");
    }
  });
});
