import { runQuery } from '../../../api/RunQuery.js';
import { displayTables } from './Tables/TableListController.js';
import { displayQuery } from './Query/QueryDisplayController.js';
import { displayLines } from './DisplayLines.js';
import { addTableResultPopupListeners } from './ResultPopupListener.js';

const stored = sessionStorage.getItem('querySession');
if (!stored) {
  location.href = '/input';
} else {
  // セッションにはクエリ情報のみ保存されているため、クエリ構造の解析はここで行う
  // （実行結果は含まない。テーブル項目クリック時にrun-query-blockで別途取得する）
  const queryInfo = JSON.parse(stored);
  const response = await runQuery(queryInfo);
  if (!response.ok) {
    location.href = '/input';
  } else {
    const data = await response.json();
    const queryBlocks = data.query_blocks;

    displayQuery(queryInfo.query);
    displayTables(queryBlocks);
    displayLines(queryBlocks);
    addTableResultPopupListeners(queryBlocks);
  }
}
