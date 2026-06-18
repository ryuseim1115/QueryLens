const dialog = document.querySelector('.csv-file-dialog');
const csvFileErrorMessage = document.querySelector('.dialog-error');
const closeCsvFileListBtn = document.querySelector('.close-btn');

export function openDialog() {
  dialog.showModal();
}

export function closeDialog() {
  csvFileErrorMessage.textContent = '';
  dialog.close();
}

closeCsvFileListBtn.addEventListener('click', () => {
  closeDialog();
});
