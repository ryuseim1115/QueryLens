import { runQuery } from '../../../api/RunQuery.js';
import { displayTables } from './Display/DisplayTables.js';
import { displayQuery } from './Display/DisplayQuery.js';
import { displayLines } from './Display/DisplayLines.js';
import { displayQueryResult } from './Display/DisplayQueryResult.js';

const stored = sessionStorage.getItem('querySession');
if (!stored) {
  location.href = '/input';
} else {
  // セッションにはクエリ情報のみ保存されているため、解析結果はここで取り直す
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
    displayQueryResult(queryBlocks);
  }
}
