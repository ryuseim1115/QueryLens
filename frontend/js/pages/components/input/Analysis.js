import { runQuery } from '../../../api/RunQuery.js';

const errorMsg = document.querySelector('.query-error');
const analysisBtn = document.querySelector('.analysis-btn');
const analysisBtnLabel = analysisBtn.textContent;

// フォームからDBタイプとクエリ文字列を取得する
function getQueryInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

// クエリエラーのメッセージを表示する
function showError(message) {
  errorMsg.textContent = message;
  errorMsg.classList.add('visible');
}

// 解析中は「解析」ボタンにローディング表示を出し、全ボタンを操作できないようにする
function setLoading(isLoading) {
  document.querySelectorAll('button').forEach((button) => {
    button.disabled = isLoading;
  });
  analysisBtn.classList.toggle('loading', isLoading);
  analysisBtn.textContent = isLoading ? '解析中' : analysisBtnLabel;
}

// 実行したクエリ情報をセッションストレージに保存する（結果画面で再実行するため）。
// 解析結果そのものは保存しない（レコード件数次第でストレージ容量を超えるため）。
function saveQuerySession(queryInfo) {
  try {
    sessionStorage.setItem('querySession', JSON.stringify(queryInfo));
  } catch {
    showError('クエリの保存に失敗しました。クエリを短くして再度お試しください。');
    return false;
  }
  return true;
}

// 「解析」ボタンが押されたときの処理
export async function handleAnalysisClick() {
  const queryInfo = getQueryInfo();
  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');
  setLoading(true);

  // 入力されたクエリをサーバーに送り、構造解析・実行を依頼する（結果画面遷移前の検証を兼ねる）
  const response = await runQuery(queryInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(error.detail);
    setLoading(false);
    return;
  }

  // 成功したら、クエリ情報をセッションに保存して結果画面へ遷移する
  if (!saveQuerySession(queryInfo)) {
    setLoading(false);
    return;
  }
  location.href = '/result';
}
