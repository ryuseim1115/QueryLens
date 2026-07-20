const dialog = document.querySelector('.file-dialog');

// ダイアログを開く
export function openDialog() {
  dialog.showModal();
}

// ダイアログを閉じる
export function closeDialog() {
  dialog.close();
}
