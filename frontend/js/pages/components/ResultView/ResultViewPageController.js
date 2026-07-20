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
  // セッションにはクエリ情報のみ保存されているため、該当ブロックの実行結果はここで取得する
  const queryInfo = JSON.parse(stored);
  const startIndex = Number(new URLSearchParams(location.search).get('start_index'));

  const response = await runQueryBlock(queryInfo, startIndex);
  if (!response.ok) {
    location.href = '/input';
  } else {
    const data = await response.json();
    const queryBlock = data.query_block;

    if (queryBlock.parent_alias) {
      document.title = `QueryLens - 実行結果: ${queryBlock.parent_alias}`;
      document.querySelector('.panel-header').textContent =
        `実行結果: ${queryBlock.parent_alias}`;
    }

    renderResultTable(queryBlock.result);
  }
}
