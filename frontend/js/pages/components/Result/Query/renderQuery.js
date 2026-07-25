import { buildLineContentHtml } from './buildLineContentHtml.js';

// 行番号つきでクエリを描画する（highlightRangesがあれば該当箇所を<mark>でハイライトする）
export function renderQuery(lineOffsets, highlightRanges) {
  const queryDisplayEl = document.querySelector('.query-display');
  queryDisplayEl.innerHTML = '';

  lineOffsets.forEach((lineOffset, index) => {
    const lineEl = document.createElement('div');
    lineEl.className = 'query-line';

    const numberEl = document.createElement('span');
    numberEl.className = 'query-line-number';
    numberEl.textContent = String(index + 1);

    const contentEl = document.createElement('span');
    contentEl.className = 'query-line-content';
    contentEl.innerHTML = buildLineContentHtml(lineOffset, highlightRanges);

    lineEl.appendChild(numberEl);
    lineEl.appendChild(contentEl);
    queryDisplayEl.appendChild(lineEl);
  });
}
