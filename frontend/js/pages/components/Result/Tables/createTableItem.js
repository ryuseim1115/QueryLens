import { highlightQuery } from '../Query/QueryDisplayController.js';

// テーブル名ボタンを1つ作る。クリックで、そのテーブルが属するクエリブロックの該当箇所をハイライトする
export function createTableItem(table, queryBlock) {
  const tableEl = document.createElement('div');
  tableEl.className = 'table-item';
  tableEl.textContent =
    table.name && table.alias
      ? `${table.name} (${table.alias})`
      : table.name || table.alias;
  tableEl.dataset.alias = table.alias || '';

  tableEl.addEventListener('click', () => {
    highlightQuery(queryBlock.start_index, queryBlock.end_index);
  });

  return tableEl;
}
