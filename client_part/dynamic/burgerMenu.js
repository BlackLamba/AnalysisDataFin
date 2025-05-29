document.addEventListener('DOMContentLoaded', () => {
  const burger = document.querySelector('.burger');
  const sidebar = document.querySelector('.sidebar');

  burger.addEventListener('click', () => {
    sidebar.classList.toggle('active');
    document.body.classList.toggle('menu-open');
  });

  // Закрыть меню при клике на затемнённую область
  document.body.addEventListener('click', (e) => {
    if (
      document.body.classList.contains('menu-open') &&
      !sidebar.contains(e.target) &&
      e.target !== burger
    ) {
      sidebar.classList.remove('active');
      document.body.classList.remove('menu-open');
    }
  });
});
