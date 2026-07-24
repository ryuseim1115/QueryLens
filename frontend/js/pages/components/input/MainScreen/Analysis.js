import { runQuery } from '../../../../api/RunQuery.js';
import { showError, clearError } from '../../../../common/ErrorMessage.js';

const errorMsg = document.querySelector('.query-error');
const analysisBtn = document.querySelector('.analysis-btn');
const analysisBtnLabel = analysisBtn.textContent;

// フォームからDBタイプとクエリ文字列を取得する
function getQueryInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

// 解析中は「解析」ボタンにローディング表示を出し、全ボタンを操作できないようにする
function setLoading(isLoading) {
  document.querySelectorAll('button').forEach((button) => {
    button.disabled = isLoading;
  });
  analysisBtn.classList.toggle('loading', isLoading);
  analysisBtn.textContent = isLoading ? '解析中' : analysisBtnLabel;
}

// クエリ情報と解析結果（クエリブロック構造）をセッションストレージに保存する
// （結果画面で使うため）。この段階の各ブロックのresultは常に[]なので、
// レコード件数によるストレージ容量超過の心配はない。
function saveQuerySession(queryInfo, queryBlocks) {
  try {
    sessionStorage.setItem('querySession', JSON.stringify({ queryInfo, queryBlocks }));
  } catch {
    showError(
      errorMsg,
      'クエリの保存に失敗しました。クエリを短くして再度お試しください。',
    );
    return false;
  }
  return true;
}

// 「解析」ボタンが押されたときの処理
export async function handleAnalysisClick() {
  const queryInfo = getQueryInfo();
  clearError(errorMsg);
  setLoading(true);

  // 入力されたクエリをサーバーに送り、構造解析を依頼する
  const response = await runQuery(queryInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(errorMsg, error.detail);
    setLoading(false);
    return;
  }

  // 成功したら、クエリ情報と解析結果をセッションに保存して結果画面へ遷移する
  const { query_blocks } = await response.json();
  if (!saveQuerySession(queryInfo, query_blocks)) {
    setLoading(false);
    return;
  }
  location.href = '/result';
}
