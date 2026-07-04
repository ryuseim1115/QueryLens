import { registerUser } from '../../api/RegisterUser.js';

const registerBtn = document.querySelector(".register-btn")
function getRegisterInfo() {
    return Object.fromEntries(new FormData(document.querySelector('form')).entries());
}
registerBtn.addEventListener('click', async () => {
    const registerInfo = getRegisterInfo();
    const response = await registerUser(registerInfo);

})


