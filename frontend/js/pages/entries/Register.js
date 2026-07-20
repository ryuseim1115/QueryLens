import { registerUser } from '../../api/RegisterUser.js';
import { showError, clearError } from '../../common/ErrorMessage.js';

const registerBtn = document.querySelector('.register-btn');
const errorMsg = document.querySelector('.register-error');

function getRegisterInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

function extractErrorMessage(detail) {
  if (typeof detail === 'string') {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail.map((e) => e.msg.replace(/^Value error,\s*/, '')).join('\n');
  }
  return '登録に失敗しました';
}

registerBtn.addEventListener('click', async () => {
  const registerInfo = getRegisterInfo();
  clearError(errorMsg);

  const response = await registerUser(registerInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(errorMsg, extractErrorMessage(error.detail));
    return;
  }

  location.href = '/login';
});
