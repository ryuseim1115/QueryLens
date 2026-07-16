import { registerUser } from '../../api/RegisterUser.js';

const registerBtn = document.querySelector('.register-btn');
const errorMsg = document.querySelector('.register-error');

function getRegisterInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

function showError(message) {
  errorMsg.textContent = message;
  errorMsg.classList.add('visible');
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
  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');

  const response = await registerUser(registerInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(extractErrorMessage(error.detail));
    return;
  }

  location.href = '/login';
});
