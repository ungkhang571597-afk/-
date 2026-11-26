(() => {
  'use strict';

  const form = document.getElementById('property-lookup');
  const input = document.getElementById('zpid');
  const error = document.getElementById('zpid-error');
  const paste = document.getElementById('paste-query');
  const submit = form.querySelector('button[type="submit"]');

  function clearError() {
    input.removeAttribute('aria-invalid');
    error.textContent = '';
  }

  function isZpid(value) {
    return /^[0-9]{1,20}$/.test(value) && /[1-9]/.test(value);
  }

  function showError(message) {
    error.textContent = message;
    input.focus();
  }

  function openProperty(zpid) {
    clearError();
    input.value = zpid;
    window.location.assign(`https://www.zillow.com/homedetails/${zpid}_zpid/`);
  }

  input.addEventListener('input', clearError);

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const zpid = input.value.trim();
    if (!isZpid(zpid)) {
      input.setAttribute('aria-invalid', 'true');
      showError(zpid ? '请输入有效的房源编号（仅限数字）。' : '请输入房源编号（ZPID）。');
      return;
    }

    openProperty(zpid);
  });

  paste.addEventListener('click', async () => {
    clearError();
    paste.disabled = true;
    submit.disabled = true;

    let zpid;
    try {
      zpid = (await navigator.clipboard.readText()).trim();
    } catch {
      showError('无法读取剪贴板，请手动粘贴编号后查询。');
      return;
    } finally {
      paste.disabled = false;
      submit.disabled = false;
    }

    if (!isZpid(zpid)) {
      showError(zpid ? '剪贴板里不是有效的房源编号。' : '剪贴板为空，请先复制房源编号。');
      return;
    }

    openProperty(zpid);
  });

  paste.disabled = false;
  submit.disabled = false;
})();
