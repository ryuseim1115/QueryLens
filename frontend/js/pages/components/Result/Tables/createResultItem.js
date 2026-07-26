import { highlightQuery } from '../Query/QueryDisplayController.js';

// テーブル一覧の末尾に置く「結果」ボックスを作る。クリックでクエリ全体をハイライトする
export function createResultItem(rootQueryBlock) {
  const resultEl = document.createElement('div');
  resultEl.className = 'table-item result-item';
  resultEl.textContent = '結果';

  resultEl.addEventListener('click', () => {
    highlightQuery([
      { start_index: rootQueryBlock.start_index, end_index: rootQueryBlock.end_index },
    ]);
  });

  return resultEl;
}
