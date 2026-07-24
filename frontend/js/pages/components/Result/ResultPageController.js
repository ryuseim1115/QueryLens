import { displayTables } from './Tables/TableListController.js';
import { displayQuery } from './Query/QueryDisplayController.js';
import { displayLines } from './DisplayLines.js';
import { addTableResultPopupListeners } from './ResultPopupListener.js';

const stored = sessionStorage.getItem('querySession');
if (!stored) {
  location.href = '/input';
} else {
  // Analysis.js（解析ボタン押下時）で解析済みのため、ここで再解析する必要はない
  const { queryInfo, queryBlocks } = JSON.parse(stored);

  displayQuery(queryInfo.query);
  displayTables(queryBlocks);
  displayLines(queryBlocks);
  addTableResultPopupListeners(queryBlocks);
}
