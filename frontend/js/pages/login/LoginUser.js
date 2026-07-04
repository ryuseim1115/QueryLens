import { authUser } from '../../api/AuthUser.js';

const loginBtn = document.querySelector('.login-btn');
const errorMsg = document.querySelector('.login-error');

function getAuthInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

function showError(message) {
  errorMsg.textContent = message;
  errorMsg.classList.add('visible');
}

loginBtn.addEventListener('click', async () => {
  const authInfo = getAuthInfo();
  errorMsg.textContent = '';
  errorMsg.classList.remove('visible');

  const response = await authUser(authInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(error.detail);
    return;
  }

  location.href = '/input';
});
