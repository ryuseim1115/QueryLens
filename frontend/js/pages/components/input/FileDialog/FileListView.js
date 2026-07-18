import { addPurgeListener } from './PurgeFileListener.js';

const fileListEl = document.querySelector('.file-list');

// 一覧の中身を空にする
export function clearFileList() {
  fileListEl.innerHTML = '';
}

// 現在一覧に表示されているファイル名を取得する
export function getFileNames() {
  return [...fileListEl.querySelectorAll('.file-row span')].map(
    (span) => span.textContent,
  );
}

// ファイル名を1件だけ一覧に追加する
export function appendFileRow(fileName) {
  const fileRowDiv = document.createElement('div');
  fileRowDiv.classList.add('file-row');

  // ファイル名を表示する部分
  const nameSpan = document.createElement('span');
  nameSpan.textContent = fileName;

  // この行を削除するためのボタン
  const deleteBtn = document.createElement('button');
  deleteBtn.type = 'button';
  deleteBtn.classList.add('delete-file-btn');
  deleteBtn.textContent = '削除';
  addPurgeListener(deleteBtn, fileName);

  fileRowDiv.appendChild(nameSpan);
  fileRowDiv.appendChild(deleteBtn);
  fileListEl.appendChild(fileRowDiv);
}
