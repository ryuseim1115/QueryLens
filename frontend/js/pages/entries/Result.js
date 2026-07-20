import '../components/Result/ResultPageController.js';

const backBtn = document.querySelector('.back-btn');

backBtn.addEventListener('click', () => {
  location.href = '/input';
});
