import { escapeHtml } from './escapeHtml.js';

// 空行でも行の高さを保つため、空文字の場合はnon-breaking spaceを入れる
function renderPlainText(text) {
  return text.length > 0 ? escapeHtml(text) : '&nbsp;';
}

// 行の表示内容(HTML)を組み立てる。highlightRangeがあればこの行に重なる部分を<mark>で囲む
export function buildLineContentHtml(lineOffset, highlightRange) {
  if (!highlightRange) {
    return renderPlainText(lineOffset.text);
  }

  // パターン1: 1文字も重なっていない（行の前で終わっている、または行の後から始まる）
  const noOverlap =
    highlightRange.end_index <= lineOffset.start_index ||
    highlightRange.start_index >= lineOffset.end_index;
  if (noOverlap) {
    return renderPlainText(lineOffset.text);
  }

  const touchesLineStart = highlightRange.start_index <= lineOffset.start_index;
  const touchesLineEnd = highlightRange.end_index >= lineOffset.end_index;

  // パターン2: 行全体に重なっている
  if (touchesLineStart && touchesLineEnd) {
    return `<mark>${escapeHtml(lineOffset.text)}</mark>`;
  }

  // パターン3: 前半（先頭〜途中）だけ重なっている
  if (touchesLineStart && !touchesLineEnd) {
    const localEnd = highlightRange.end_index - lineOffset.start_index;
    const markedText = escapeHtml(lineOffset.text.slice(0, localEnd));
    const afterMark = escapeHtml(lineOffset.text.slice(localEnd));
    return `<mark>${markedText}</mark>${afterMark}`;
  }

  // パターン4: 後半（途中〜末尾）だけ重なっている
  if (!touchesLineStart && touchesLineEnd) {
    const localStart = highlightRange.start_index - lineOffset.start_index;
    const beforeMark = escapeHtml(lineOffset.text.slice(0, localStart));
    const markedText = escapeHtml(lineOffset.text.slice(localStart));
    return `${beforeMark}<mark>${markedText}</mark>`;
  }

  // パターン5: 真ん中（途中〜途中）だけ重なっている
  const localStart = highlightRange.start_index - lineOffset.start_index;
  const localEnd = highlightRange.end_index - lineOffset.start_index;
  const beforeMark = escapeHtml(lineOffset.text.slice(0, localStart));
  const markedText = escapeHtml(lineOffset.text.slice(localStart, localEnd));
  const afterMark = escapeHtml(lineOffset.text.slice(localEnd));
  return `${beforeMark}<mark>${markedText}</mark>${afterMark}`;
}
