import { runQueryBlock } from '../../../api/RunQueryBlock.js';
import { renderResultError, renderResultTable } from './RenderResultTable.js';

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

    const resultLabel =
      queryBlock.parent_alias || (queryBlock.depth === 0 ? '結果' : null);
    if (resultLabel) {
      document.title = `QueryLens - 実行結果: ${resultLabel}`;
      document.querySelector('.panel-header').textContent = `実行結果: ${resultLabel}`;
    }

    if (!response.ok) {
      const body = await response.json().catch(() => null);
      renderResultError(body?.detail ?? 'クエリの実行に失敗しました');
    } else {
      const { records, truncated } = await response.json();
      renderResultTable(records, truncated);
    }
  }
}
