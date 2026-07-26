import { escapeHtml } from './escapeHtml.js';

// 空行でも行の高さを保つため、空文字の場合はnon-breaking spaceを入れる
function renderPlainText(text) {
  return text.length > 0 ? escapeHtml(text) : '&nbsp;';
}

// highlightRangesのうちこの行に重なる部分を、行内のローカル座標(0〜text.length)に変換する。
// 範囲同士が重なっている場合は1つにマージする
function toLocalRanges(highlightRanges, lineOffset) {
  const localRanges = highlightRanges
    .filter(
      (range) =>
        range.end_index > lineOffset.start_index &&
        range.start_index < lineOffset.end_index,
    )
    .map((range) => ({
      start: Math.max(0, range.start_index - lineOffset.start_index),
      end: Math.min(lineOffset.text.length, range.end_index - lineOffset.start_index),
    }))
    .sort((a, b) => a.start - b.start);

  const merged = [];
  for (const range of localRanges) {
    const last = merged[merged.length - 1];
    if (last && range.start <= last.end) {
      last.end = Math.max(last.end, range.end);
    } else {
      merged.push(range);
    }
  }
  return merged;
}

// 行の表示内容(HTML)を組み立てる。highlightRangesがあればこの行に重なる部分を<mark>で囲む
export function buildLineContentHtml(lineOffset, highlightRanges) {
  if (!highlightRanges || highlightRanges.length === 0) {
    return renderPlainText(lineOffset.text);
  }

  const localRanges = toLocalRanges(highlightRanges, lineOffset);
  if (localRanges.length === 0) {
    return renderPlainText(lineOffset.text);
  }

  let html = '';
  let cursor = 0;
  for (const { start, end } of localRanges) {
    html += escapeHtml(lineOffset.text.slice(cursor, start));
    html += `<mark>${escapeHtml(lineOffset.text.slice(start, end))}</mark>`;
    cursor = end;
  }
  html += escapeHtml(lineOffset.text.slice(cursor));

  return html;
}
