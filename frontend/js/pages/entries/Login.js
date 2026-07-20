import { authUser } from '../../api/AuthUser.js';
import { showError, clearError } from '../../common/ErrorMessage.js';

const loginBtn = document.querySelector('.login-btn');
const errorMsg = document.querySelector('.login-error');

function getAuthInfo() {
  return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}

loginBtn.addEventListener('click', async () => {
  const authInfo = getAuthInfo();
  clearError(errorMsg);

  const response = await authUser(authInfo);
  if (!response.ok) {
    const error = await response.json();
    showError(errorMsg, error.detail);
    return;
  }

  location.href = '/input';
});
