const copyButton = document.querySelector('.copy-install');
copyButton.addEventListener('click', async () => {
  const status = document.querySelector('.copy-status');
  try {
    await navigator.clipboard.writeText(document.querySelector('#linux-install').textContent);
    status.textContent = 'Copied';
  } catch {
    status.textContent = 'Copy failed; select the commands instead.';
  }
});
