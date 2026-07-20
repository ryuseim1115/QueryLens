const queryTextarea = document.querySelector('textarea[name="query"]');
const lineNumbersEl = document.querySelector('.query-line-numbers');

// クエリの行数に合わせて、行番号ガター（1, 2, 3...）を再生成する
export function updateLineNumbers() {
  const lineCount = queryTextarea.value.split('\n').length;
  const numbers = [];
  for (let i = 1; i <= lineCount; i += 1) {
    numbers.push(i);
  }
  lineNumbersEl.textContent = numbers.join('\n');
}

// ガター(lineNumbersEl)はoverflow:hiddenでユーザー操作ではスクロールできないため、
// 実際にスクロールされたqueryTextarea側のscrollTopを都度コピーし、スクロールしたことにする
export function syncScroll() {
  lineNumbersEl.scrollTop = queryTextarea.scrollTop;
}
