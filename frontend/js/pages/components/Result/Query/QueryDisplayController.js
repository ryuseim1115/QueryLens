import { splitLinesWithOffsets } from './splitLinesWithOffsets.js';
import { renderQuery } from './renderQuery.js';

// { text, start_index, end_index } start_index/end_indexは元クエリ文字列内の文字オフセット
let _queryLineOffsets = [];

export function displayQuery(query) {
  _queryLineOffsets = splitLinesWithOffsets(query);
  renderQuery(_queryLineOffsets, null);
}

export function highlightQuery(start_index, end_index) {
  renderQuery(_queryLineOffsets, { start_index, end_index });
}
