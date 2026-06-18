import { runQuery } from '../../api/RunQuery.js';

const errorMsg = document.querySelector('.query-error');

function getQueryInfo() {
  return Object.fromEntries(
    new FormData(document.querySelector('form')).entries(),
  );
}

function showError(message) {
  errorMsg.textContent = message;
  errorMsg.classList.add('visible');
}

function saveQuerySession(query, subqueries) {
  sessionStorage.setItem(
    'querySession',
    JSON.stringify({ query, subqueryResults: subqueries }),
  );
}

document.querySelector('.analysis-btn').addEventListener('click', async () => {
  const queryInfo = getQueryInfo();
  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');

  const response = await runQuery(queryInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(error.detail);
    return;
  }

  const data = await response.json();
  saveQuerySession(queryInfo.query, data.subqueries);
  location.href = '/result';
});
