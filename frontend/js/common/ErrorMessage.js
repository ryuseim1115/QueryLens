// エラーメッセージ要素にメッセージを表示する
export function showError(errorMsg, message) {
  errorMsg.textContent = message;
  errorMsg.classList.add('visible');
}

// エラーメッセージ要素の表示をクリアする
export function clearError(errorMsg) {
  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');
}
