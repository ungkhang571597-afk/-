(() => {
  'use strict';

  const form = document.getElementById('property-lookup');
  const input = document.getElementById('zpid');
  const error = document.getElementById('zpid-error');

  input.addEventListener('input', () => {
    input.removeAttribute('aria-invalid');
    error.textContent = '';
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const zpid = input.value.trim();
    if (!/^[0-9]{1,20}$/.test(zpid) || !/[1-9]/.test(zpid)) {
      input.setAttribute('aria-invalid', 'true');
      error.textContent = zpid ? '请输入有效的房源编号（仅限数字）。' : '请输入房源编号（ZPID）。';
      input.focus();
      return;
    }

    window.location.assign(`https://www.zillow.com/homedetails/${zpid}_zpid/`);
  });

  form.querySelector('button[type="submit"]').disabled = false;
})();
