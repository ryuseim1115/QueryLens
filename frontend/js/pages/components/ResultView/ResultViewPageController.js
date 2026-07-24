import { runQueryBlock } from '../../../api/RunQueryBlock.js';
import { renderResultTable } from './RenderResultTable.js';

function requestQuerySessionFromOpener() {
  if (!window.opener) return Promise.resolve(null);

  return new Promise((resolve) => {
    function handleMessage(event) {
      if (event.origin !== location.origin || event.data?.type !== 'query-session')
        return;
      window.removeEventListener('message', handleMessage);
      resolve(event.data.payload);
    }
    window.addEventListener('message', handleMessage);
    window.opener.postMessage({ type: 'query-session-request' }, location.origin);
  });
}

const stored =
  sessionStorage.getItem('querySession') ?? (await requestQuerySessionFromOpener());

if (!stored) {
  location.href = '/input';
} else {
  // セッションには解析結果（クエリブロック構造）が含まれているため、
  // 該当ブロックはここで特定する（サーバー側での再解析は不要）
  const { queryInfo, queryBlocks } = JSON.parse(stored);
  const startIndex = Number(new URLSearchParams(location.search).get('start_index'));
  const queryBlock = queryBlocks.find((qb) => qb.start_index === startIndex);

  if (!queryBlock) {
    location.href = '/input';
  } else {
    const response = await runQueryBlock({
      databaseType: queryInfo.databaseType,
      query: queryBlock.query,
    });
    if (!response.ok) {
      location.href = '/input';
    } else {
      const { records } = await response.json();

      if (queryBlock.parent_alias) {
        document.title = `QueryLens - 実行結果: ${queryBlock.parent_alias}`;
        document.querySelector('.panel-header').textContent =
          `実行結果: ${queryBlock.parent_alias}`;
      }

      renderResultTable(records);
    }
  }
}
