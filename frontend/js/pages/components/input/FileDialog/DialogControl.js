const dialog = document.querySelector('.file-dialog');
const closeFileListBtn = document.querySelector('.close-btn');

// ダイアログを開く
export function openDialog() {
  dialog.showModal();
}

// ダイアログを閉じる
export function closeDialog() {
  dialog.close();
}

// 「閉じる」ボタンが押されたらダイアログを閉じる
closeFileListBtn.addEventListener('click', () => {
  closeDialog();
});
