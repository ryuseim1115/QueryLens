const queryTextarea = document.querySelector('textarea[name="query"]');
const lineNumbersEl = document.querySelector('.query-line-numbers');

// クエリの行数に合わせて、行番号ガター（1, 2, 3...）を再生成する
function updateLineNumbers() {
  const lineCount = queryTextarea.value.split('\n').length;
  const numbers = [];
  for (let i = 1; i <= lineCount; i += 1) {
    numbers.push(i);
  }
  lineNumbersEl.textContent = numbers.join('\n');
}

// テキストエリアのスクロールに、行番号ガターのスクロール位置を追従させる
function syncScroll() {
  lineNumbersEl.scrollTop = queryTextarea.scrollTop;
}

queryTextarea.addEventListener('input', updateLineNumbers);
queryTextarea.addEventListener('scroll', syncScroll);

updateLineNumbers();
