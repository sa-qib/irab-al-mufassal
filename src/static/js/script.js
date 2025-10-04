// font control 
(function(){
  // elements (may be null if not present)
  const themeToggle = document.getElementById('theme-toggle');
  const moonIcon = document.getElementById('moon-icon');
  const sunIcon = document.getElementById('sun-icon');

  // main content container that should be scaled
  const mainContent = document.querySelector('main .max-w-3xl') 
                   || document.querySelector('main .max-w-4xl')
                   || document.querySelector('main .max-w-2xl')
                   || document.querySelector('main > div');

  const fontSizeInput = document.getElementById('fontSizeInput');

  // load persisted values (fallback default 16px)
  let currentFontSize = parseFloat(localStorage.getItem('siteFontSize'));
  if (!currentFontSize || isNaN(currentFontSize)) {
    currentFontSize = 36; // first-visit default
    
    if (isNaN(currentFontSize)) currentFontSize = 36;

  }

  // THEMES
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('theme', theme); } catch(e){}
    // toggle icons if present (show sun for light/sunset)
    if (moonIcon && sunIcon) {
      if (['sunset','light'].includes(theme)) {
        moonIcon.classList.add('hidden'); sunIcon.classList.remove('hidden');
      } else {
        sunIcon.classList.add('hidden'); moonIcon.classList.remove('hidden');
      }
    }
  }

  // initialize theme: prefer stored user choice, otherwise default 'retro'
  const storedTheme = localStorage.getItem('theme') || 'retro';
  setTheme(storedTheme);

  // theme toggle (cycles through a short list)
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const order = ['retro','sunset'];
      const current = document.documentElement.getAttribute('data-theme') || 'retro';
      const idx = order.indexOf(current);
      const next = order[(idx + 1) % order.length];
      setTheme(next);
    });
  }

  // FONT SIZE CONTROLS (apply only to main content)
  function applyFontSize() {
    if (!mainContent) return;
    try { localStorage.setItem('siteFontSize', currentFontSize); } catch(e){}
    // set a base on the container (useful for inheritance)
    mainContent.style.fontSize = currentFontSize + 'px';

    // mapping of multipliers by tag (so headings scale proportionally)
    const multipliers = {
      'h1': 2,
      'h2': 1.5,
      'h3': 1.25,
      'h4': 1,
      'h5': 0.875,
      'h6': 0.75,
      'p': 1
    };

    // override inline sizes for text elements inside the content area
    mainContent.querySelectorAll('h1,h2,h3,h4,h5,h6,p').forEach(el => {
      const tag = el.tagName.toLowerCase();
      let mul = multipliers[tag] || 1;
      // make ayah-lines (usually font-semibold) slightly larger
      if (tag === 'p' && el.classList.contains('font-semibold')) mul = 1.25;
      el.style.fontSize = (currentFontSize * mul) + 'px';
    });

    if (fontSizeInput) fontSizeInput.value = Math.round(currentFontSize);
  }

  // change font size by delta (positive/negative)
  function changeFontSize(delta) {
    currentFontSize = (currentFontSize || 16) + delta;
    if (currentFontSize < 16) currentFontSize = 16; // small safeguard
    applyFontSize();
  }

  // set explicit size (in px)
  function setFontSize(size) {
    const s = parseFloat(size);
    if (!isNaN(s)) currentFontSize = s;
    if (currentFontSize < 16) currentFontSize = 16;
    applyFontSize();
  }

  // expose for inline onclicks / HTML controls
  window.setTheme = setTheme;
  window.changeFontSize = changeFontSize;
  window.setFontSize = setFontSize;

  // wire input if present
  if (fontSizeInput) {
    fontSizeInput.addEventListener('change', e => setFontSize(e.target.value));
  }

  // initialize once DOM is ready (and also call immediately)
  document.addEventListener('DOMContentLoaded', applyFontSize);
  applyFontSize();
})();


// open/close right drawer on keyboard shortcuts 

