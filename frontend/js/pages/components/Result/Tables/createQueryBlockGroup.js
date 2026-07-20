import { createTableItem } from './createTableItem.js';

// 1つのクエリブロックに属するテーブル項目群をまとめた要素を作る
export function createQueryBlockGroup(queryBlock) {
  const queryBlockGroupEl = document.createElement('div');
  queryBlockGroupEl.className = 'query-block-group';
  queryBlockGroupEl.dataset.startIndex = queryBlock.start_index;

  queryBlock.tables_name_alias.forEach((table) => {
    queryBlockGroupEl.appendChild(createTableItem(table, queryBlock));
  });

  return queryBlockGroupEl;
}
