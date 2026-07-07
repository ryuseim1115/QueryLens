import { findParentAliasEl } from '../../../common/SubqueryDomFinder.js';

const RESULT_WINDOW_NAME = 'queryLensResult';
const POPUP_WIDTH = 960;
const POPUP_HEIGHT = 640;

window.addEventListener('message', (event) => {
  if (event.origin !== location.origin || event.data?.type !== 'query-session-request') return;
  event.source.postMessage(
    { type: 'query-session', payload: sessionStorage.getItem('querySession') },
    location.origin,
  );
});

export function displayQueryResult(subqueries) {
  subqueries.forEach((subquery) => {
    const parentAlias = findParentAliasEl(subquery);
    if (!parentAlias) return;
    parentAlias.addEventListener('click', () => openResultPopup(subquery));
  });
}

function openResultPopup(subquery) {
  const left = Math.max(0, (window.screen.width - POPUP_WIDTH) / 2);
  const top = Math.max(0, (window.screen.height - POPUP_HEIGHT) / 2);
  const features = `width=${POPUP_WIDTH},height=${POPUP_HEIGHT},left=${left},top=${top},resizable=yes,scrollbars=yes`;
  const table = encodeURIComponent(subquery.parent_alias ?? '');

  window.open(
    `/result-view?table=${table}&start_index=${subquery.start_index}`,
    RESULT_WINDOW_NAME,
    features,
  );
}
