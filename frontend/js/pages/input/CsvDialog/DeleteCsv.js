import { deleteCsv } from '../../../api/DeleteCsv.js';

export function addDeleteListener(button, fileName) {
  button.addEventListener('click', async () => {
    button.disabled = true;
    const loadingSpan = document.createElement('span');
    loadingSpan.textContent = ' 削除中...';
    button.after(loadingSpan);

    await deleteCsv(fileName);

    button.closest('.csv-file-row').remove();
  });
}
