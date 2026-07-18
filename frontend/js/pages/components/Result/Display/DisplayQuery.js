let _lines = []; // { text, start, end } start/endは元クエリ文字列内の文字オフセット（endは改行を含まない）

// クエリ文字列を行ごとに分割し、各行の元クエリ内でのオフセットを記録する
function computeLines(query) {
  const lines = [];
  let offset = 0;
  query.split('\n').forEach((text) => {
    const start = offset;
    const end = start + text.length;
    lines.push({ text, start, end });
    offset = end + 1; // +1 は改行文字の分
  });
  return lines;
}

function escapeHtml(text) {
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// 行番号つきでクエリを描画する（highlightRangeがあれば該当箇所を<mark>でハイライトする）
function render(highlightRange) {
  const queryDisplayEl = document.querySelector('.query-display');
  queryDisplayEl.innerHTML = '';

  _lines.forEach((line, index) => {
    const lineEl = document.createElement('div');
    lineEl.className = 'query-line';

    const numberEl = document.createElement('span');
    numberEl.className = 'query-line-number';
    numberEl.textContent = String(index + 1);

    const contentEl = document.createElement('span');
    contentEl.className = 'query-line-content';

    // ハイライト範囲を行内のローカルなオフセットに変換し、この行に重なる部分だけ<mark>で囲む
    const localStart = highlightRange
      ? Math.min(Math.max(highlightRange.start_index - line.start, 0), line.text.length)
      : 0;
    const localEnd = highlightRange
      ? Math.min(Math.max(highlightRange.end_index - line.start, 0), line.text.length)
      : 0;

    if (highlightRange && localStart < localEnd) {
      const before = escapeHtml(line.text.slice(0, localStart));
      const marked = escapeHtml(line.text.slice(localStart, localEnd));
      const after = escapeHtml(line.text.slice(localEnd));
      contentEl.innerHTML = `${before}<mark>${marked}</mark>${after}`;
    } else {
      // 空行でも行の高さを保つため、空文字の場合はnon-breaking spaceを入れる
      contentEl.innerHTML = line.text.length > 0 ? escapeHtml(line.text) : '&nbsp;';
    }

    lineEl.appendChild(numberEl);
    lineEl.appendChild(contentEl);
    queryDisplayEl.appendChild(lineEl);
  });
}

export function displayQuery(query) {
  _lines = computeLines(query);
  render(null);
}

export function highlightQuery(start_index, end_index) {
  render({ start_index, end_index });
}
