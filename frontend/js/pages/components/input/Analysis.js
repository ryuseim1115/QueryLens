import { runQuery } from '../../../api/RunQuery.js';

const errorMsg = document.querySelector('.query-error');

// フォームからDBタイプとクエリ文字列を取得する
function getQueryInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

// クエリエラーのメッセージを表示する
function showError(message) {
  errorMsg.textContent = message;
  errorMsg.classList.add('visible');
}

// 実行したクエリと、その解析結果をセッションストレージに保存する（結果画面で読み出すため）
function saveQuerySession(query, queryBlocks) {
  sessionStorage.setItem(
    'querySession',
    JSON.stringify({ query, queryBlockResults: queryBlocks }),
  );
}

// 「解析」ボタンが押されたときの処理
export async function handleAnalysisClick() {
  const queryInfo = getQueryInfo();
  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');

  // 入力されたクエリをサーバーに送り、構造解析・実行を依頼する
  const response = await runQuery(queryInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(error.detail);
    return;
  }

  // 成功したら、結果をセッションに保存して結果画面へ遷移する
  const data = await response.json();
  saveQuerySession(queryInfo.query, data.query_blocks);
  location.href = '/result';
}
