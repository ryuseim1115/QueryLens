import { displayTables } from './Display/DisplayTables.js';
import { displayQuery } from './Display/DisplayQuery.js';
import { displayLines } from './Display/DisplayLines.js';
import { displayQueryResult } from './Display/DisplayQueryResult.js';

const stored = sessionStorage.getItem('querySession');
if (!stored) {
  location.href = '/input';
} else {
  const parsed = JSON.parse(stored);
  const query = parsed.query;
  const queryBlocks = parsed.queryBlockResults;

  displayQuery(query);
  displayTables(queryBlocks);
  displayLines(queryBlocks);
  displayQueryResult(queryBlocks);
}
