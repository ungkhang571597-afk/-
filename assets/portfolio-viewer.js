(() => {
  'use strict';
  const total = 20;
  const slide = document.getElementById('slide');
  const frame = document.getElementById('slide-frame');
  const select = document.getElementById('page-select');
  const thumbs = document.getElementById('thumbnails');
  const toggle = document.getElementById('grid-toggle');
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const caption = document.getElementById('slide-title');
  const zoom = document.getElementById('zoom-dialog');
  let current = 1;
  const source = (page) => `assets/portfolio/slide-${String(page).padStart(2, '0')}.webp`;
  function show(page, updateUrl = true) {
    current = Math.min(total, Math.max(1, Number(page) || 1));
    frame.dataset.loading = 'true';
    slide.src = source(current);
    slide.alt = `作品集第${current}页`;
    if (slide.complete && slide.naturalWidth) frame.dataset.loading = 'false';
    select.value = String(current);
    prev.disabled = current === 1;
    next.disabled = current === total;
    document.getElementById('page-count').textContent = `${String(current).padStart(2, '0')} / ${total}`;
    caption.textContent = current === 1 ? '钟滔新媒体运营作品集' : `内容获客与项目实践 · 第 ${current} 页`;
    caption.classList.remove('viewer-error');
    thumbs.querySelectorAll('button').forEach((button, i) => {
      if (i + 1 === current) button.setAttribute('aria-current', 'page');
      else button.removeAttribute('aria-current');
    });
    if (updateUrl) history.replaceState(null, '', `#page=${current}`);
    if (current < total) new Image().src = source(current + 1);
  }
  for (let page = 1; page <= total; page++) {
    select.add(new Option(`${page} / ${total}`, String(page)));
    const button = document.createElement('button');
    button.className = 'thumbnail';
    button.setAttribute('aria-label', `第${page}页`);
    const image = document.createElement('img');
    image.src = source(page);
    image.alt = '';
    image.loading = 'lazy';
    image.width = 320;
    image.height = 180;
    const label = document.createElement('span');
    label.textContent = String(page).padStart(2, '0');
    button.append(image, label);
    button.addEventListener('click', () => {
      show(page);
      document.querySelector('.viewer-stage').scrollIntoView({ block: 'start' });
    });
    thumbs.append(button);
  }
  slide.addEventListener('load', () => { frame.dataset.loading = 'false'; });
  slide.addEventListener('error', () => {
    frame.dataset.loading = 'false';
    caption.textContent = '页面加载失败，可刷新重试或下载 PDF。';
    caption.classList.add('viewer-error');
  });
  prev.addEventListener('click', () => show(current - 1));
  next.addEventListener('click', () => show(current + 1));
  select.addEventListener('change', () => show(select.value));
  toggle.addEventListener('click', () => {
    thumbs.hidden = !thumbs.hidden;
    toggle.setAttribute('aria-expanded', String(!thumbs.hidden));
  });
  document.getElementById('zoom').addEventListener('click', () => {
    document.getElementById('zoom-image').src = source(current);
    zoom.showModal();
    zoom.querySelector('.zoom-scroll').scrollTo(0, 0);
  });
  document.getElementById('zoom-close').addEventListener('click', () => zoom.close());
  document.getElementById('fullscreen').addEventListener('click', async () => {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (frame.requestFullscreen) await frame.requestFullscreen();
    } catch (_) { document.getElementById('zoom').click(); }
  });
  document.addEventListener('keydown', (event) => {
    if (zoom.open || ['SELECT', 'INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
      event.preventDefault();
      show(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  let touch = null;
  frame.addEventListener('touchstart', (event) => {
    if (event.touches.length !== 1) { touch = null; return; }
    touch = { x: event.touches[0].clientX, y: event.touches[0].clientY };
  }, { passive: true });
  frame.addEventListener('touchend', (event) => {
    if (!touch || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX - touch.x;
    const dy = event.changedTouches[0].clientY - touch.y;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(current + (dx < 0 ? 1 : -1));
    touch = null;
  }, { passive: true });
  const fromHash = () => show(new URLSearchParams(location.hash.slice(1)).get('page'), false);
  window.addEventListener('hashchange', fromHash);
  fromHash();
  [select, toggle, document.getElementById('zoom'), document.getElementById('fullscreen')].forEach((control) => { control.disabled = false; });
})();
