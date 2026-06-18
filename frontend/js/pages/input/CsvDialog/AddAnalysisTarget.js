import { createTable } from '../../../api/CreateTable.js';
import { dropTable } from '../../../api/DropTable.js';

export function addAnalysisTargetListener(checkbox, fileName) {
  checkbox.addEventListener('change', async () => {
    checkbox.disabled = true;
    const loadingSpan = document.createElement('span');
    loadingSpan.textContent = ' 処理中...';
    checkbox.closest('label').appendChild(loadingSpan);

    if (checkbox.checked) {
      await createTable(fileName);
    } else {
      await dropTable(fileName);
    }

    loadingSpan.remove();
    checkbox.disabled = false;
  });
}
