const THEME_KEY = 'ondrej-theme';

function getTheme() {
  return localStorage.getItem(THEME_KEY) || 'mocha';
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  const knob = document.querySelector('.theme-knob');
  if (knob) knob.textContent = theme === 'mocha' ? '🌙' : '☀️';
}

function toggleTheme() {
  const next = getTheme() === 'mocha' ? 'latte' : 'mocha';
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
}

document.addEventListener('DOMContentLoaded', () => {
  applyTheme(getTheme());

  const btn = document.getElementById('theme-toggle');
  if (btn) btn.addEventListener('click', toggleTheme);

  // Portfolio filter
  const filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        document.querySelectorAll('[data-cat]').forEach(card => {
          card.style.display = (filter === 'all' || card.dataset.cat === filter) ? '' : 'none';
        });
      });
    });
  }
});
