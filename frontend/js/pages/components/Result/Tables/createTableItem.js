import { highlightQuery } from '../Query/QueryDisplayController.js';

// テーブル名ボタンを1つ作る。クリックで、クエリ内のそのテーブル名/エイリアス自体をハイライトする
export function createTableItem(table, queryBlock) {
  const tableEl = document.createElement('div');
  tableEl.className = 'table-item';
  tableEl.textContent =
    table.table_name && table.alias
      ? `${table.table_name} (${table.alias})`
      : table.table_name || table.alias;
  tableEl.dataset.alias = table.alias || '';

  tableEl.addEventListener('click', () => {
    if (table.start_index == null || table.end_index == null) {
      highlightQuery([
        { start_index: queryBlock.start_index, end_index: queryBlock.end_index },
      ]);
      return;
    }

    const hasReferencedBlock =
      table.referenced_block_start_index != null &&
      table.referenced_block_end_index != null;

    // サブクエリの場合、定義本体の直後にエイリアスが続く(例: "(...) AS r")ため、
    // 定義本体の開始からエイリアスの終わりまでをASも含めてひと続きにハイライトする
    const isSubqueryAliasReference = !table.table_name && table.alias;
    if (hasReferencedBlock && isSubqueryAliasReference) {
      highlightQuery([
        { start_index: table.referenced_block_start_index, end_index: table.end_index },
      ]);
      return;
    }

    const ranges = [{ start_index: table.start_index, end_index: table.end_index }];
    if (hasReferencedBlock) {
      ranges.push({
        start_index: table.referenced_block_start_index,
        end_index: table.referenced_block_end_index,
      });
    }
    highlightQuery(ranges);
  });

  return tableEl;
}
