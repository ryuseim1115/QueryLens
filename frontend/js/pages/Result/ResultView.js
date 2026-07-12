import { renderResultTable } from './Display/RenderResultTable.js';

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
  const parsed = JSON.parse(stored);
  const startIndex = Number(new URLSearchParams(location.search).get('start_index'));
  const queryBlock = parsed.queryBlockResults.find(
    (qb) => qb.start_index === startIndex,
  );

  if (queryBlock?.parent_alias) {
    document.title = `QueryLens - 実行結果: ${queryBlock.parent_alias}`;
    document.querySelector('.panel-header').textContent =
      `実行結果: ${queryBlock.parent_alias}`;
  }

  renderResultTable(queryBlock ? queryBlock.result : null);
}
