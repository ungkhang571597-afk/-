(() => {
  'use strict';
  const pages = [...document.querySelectorAll('.document-page')];
  const select = document.getElementById('page-select');
  const toolbar = document.querySelector('.viewer-toolbar');
  const zoomButton = document.getElementById('zoom');
  const zoom = document.getElementById('zoom-dialog');
  const zoomImage = document.getElementById('zoom-image');
  let current = 1;
  let scheduled = false;

  function setCurrent(page) {
    current = page;
    select.value = String(page);
    zoomButton.setAttribute('aria-label', `放大第${page}页`);
    zoomButton.title = `放大第${page}页`;
  }

  function jump(page) {
    const number = Math.min(pages.length, Math.max(1, parseInt(page, 10) || 1));
    setCurrent(number);
    pages[number - 1].scrollIntoView({ block: 'start', behavior: 'instant' });
  }

  // Track the page at the reading position while preserving normal scrolling.
  function trackPage() {
    scheduled = false;
    const top = toolbar.getBoundingClientRect().bottom;
    const line = top + Math.min(180, (innerHeight - top) * .25);
    const visible = pages.find((page) => page.getBoundingClientRect().bottom > line);
    const atEnd = scrollY + innerHeight >= document.documentElement.scrollHeight - 2;
    const number = atEnd ? pages.length : (visible ? Number(visible.dataset.page) : pages.length);
    if (number !== current) setCurrent(number);
    if (location.hash !== `#page=${number}`) history.replaceState(null, '', `#page=${number}`);
  }

  function scheduleTracking() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(trackPage);
    }
  }

  pages.forEach((page, index) => {
    select.add(new Option(`${index + 1} / ${pages.length}`, String(index + 1)));
    page.querySelector('img').addEventListener('error', () => {
      if (page.querySelector('.page-error')) return;
      const message = document.createElement('p');
      message.className = 'page-error';
      message.textContent = `第${index + 1}页加载失败，可刷新重试或下载 PDF。`;
      page.append(message);
    });
  });

  select.addEventListener('change', () => jump(select.value));
  window.addEventListener('scroll', scheduleTracking, { passive: true });
  window.addEventListener('resize', scheduleTracking, { passive: true });
  window.addEventListener('pageshow', scheduleTracking);
  const fromHash = () => jump(new URLSearchParams(location.hash.slice(1)).get('page'));
  window.addEventListener('hashchange', fromHash);

  zoomButton.addEventListener('click', () => {
    const image = pages[current - 1].querySelector('img');
    zoomImage.src = image.src;
    zoomImage.alt = `作品集第${current}页，放大查看`;
    zoom.showModal();
    zoom.querySelector('.zoom-scroll').scrollTo(0, 0);
  });
  document.getElementById('zoom-close').addEventListener('click', () => zoom.close());

  setCurrent(1);
  select.disabled = false;
  zoomButton.disabled = false;
  if (location.hash) fromHash();
})();
