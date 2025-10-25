document.addEventListener('DOMContentLoaded', function () {
  const buttons = document.querySelectorAll('.mega-btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => toggleMenu(btn));

    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { closeAll(); btn.focus(); }
      if (e.key === 'ArrowDown') { openAndFocusFirst(btn); e.preventDefault(); }
      if (e.key === 'ArrowUp') { openAndFocusLast(btn); e.preventDefault(); }
    });
  });

  // Fecha ao clicar fora
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.mega-nav')) closeAll();
  });

  function closeAll() {
    document.querySelectorAll('.mega-category.open').forEach(i => {
      i.classList.remove('open');
      const btn = i.querySelector('.mega-btn');
      if (btn) btn.setAttribute('aria-expanded', 'false');
    });
  }

  function toggleMenu(btn) {
    const li = btn.closest('.mega-category');
    const isOpen = li.classList.contains('open');
    closeAll();
    if (!isOpen) {
      li.classList.add('open');
      btn.setAttribute('aria-expanded', 'true');
      // foco no primeiro item
      const firstLink = li.querySelector('.mega-sub a');
      if (firstLink) firstLink.focus();
    }
  }

  function openAndFocusFirst(btn) { toggleMenu(btn); }
  function openAndFocusLast(btn) {
    const li = btn.closest('.mega-category');
    if (!li.classList.contains('open')) toggleMenu(btn);
    const links = li.querySelectorAll('.mega-sub a');
    if (links.length) links[links.length-1].focus();
  }
});
