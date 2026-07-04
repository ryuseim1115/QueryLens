import { uploadCsv } from '../../../api/UploadCsv.js';
import { reloadCsvFileList } from './CsvFileList.js';

const fileInput = document.querySelector('.upload-csv-input');
const selectFileBtn = document.querySelector('.select-csv-btn');
const uploadBtn = document.querySelector('.upload-csv-btn');
const fileNameLabel = document.querySelector('.upload-csv-filename');
const statusMsg = document.querySelector('.upload-csv-status');

function showStatus(message, isError) {
  statusMsg.textContent = message;
  statusMsg.classList.toggle('error', isError);
}

function resetFileSelection() {
  fileInput.value = '';
  fileNameLabel.textContent = '';
  uploadBtn.disabled = true;
}

selectFileBtn.addEventListener('click', () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  fileNameLabel.textContent = file ? file.name : '';
  uploadBtn.disabled = !file;
  showStatus('', false);
});

uploadBtn.addEventListener('click', async () => {
  const file = fileInput.files[0];
  if (!file) {
    return;
  }

  selectFileBtn.disabled = true;
  uploadBtn.disabled = true;
  showStatus('アップロード中...', false);

  const response = await uploadCsv(file);
  if (!response.ok) {
    const error = await response.json();
    showStatus(error.detail, true);
    selectFileBtn.disabled = false;
    uploadBtn.disabled = false;
    return;
  }

  showStatus('アップロード完了 ✓', false);
  resetFileSelection();
  selectFileBtn.disabled = false;
  await reloadCsvFileList();
});
