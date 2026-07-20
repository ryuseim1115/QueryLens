import { uploadCsv } from '../../../../api/UploadCsv.js';
import { importFile } from './CreateTables.js';
import {
  getDuplicateFileNames,
  describeDuplicateFileNames,
} from './DuplicateFileCheck.js';

const nativeFileInput = document.querySelector('.upload-file-input');
const selectFileBtn = document.querySelector('.select-file-btn');
const uploadBtn = document.querySelector('.upload-file-btn');
const closeFileListBtn = document.querySelector('.close-btn');
const fileNameLabel = document.querySelector('.upload-file-filename');
const statusMsg = document.querySelector('.upload-file-status');
const loadingStatus = document.querySelector('.loading-status');

// アップロード状況のメッセージを表示する（isErrorがtrueならエラー用の色にする）
export function showStatus(message, isError) {
  statusMsg.textContent = message;
  statusMsg.classList.toggle('error', isError);
}

// 選択中のファイル数に応じて、表示用の文言を組み立てる
function describeSelectedFiles(files) {
  if (files.length === 0) {
    return '';
  }
  if (files.length === 1) {
    return files[0].name;
  }
  return `${files.length}個のファイル`;
}

// ファイル選択状態と、それに紐づく表示をリセットする
function resetFileSelection() {
  nativeFileInput.value = '';
  fileNameLabel.textContent = '';
  uploadBtn.disabled = true;
}

// ファイル選択ボタンを押下したら、ネイティブのファイル選択ダイアログを表示する
export function handleSelectFileClick() {
  nativeFileInput.click();
}

// ネイティブのファイル選択ダイアログでファイルが選択されたら、ファイル名表示・アップロードボタンの有効/無効・重複チェックを更新する
export function handleFileInputChange() {
  const files = Array.from(nativeFileInput.files);
  fileNameLabel.textContent = describeSelectedFiles(files);
  uploadBtn.disabled = files.length === 0;

  const duplicateNames = getDuplicateFileNames(files);
  showStatus(
    duplicateNames.length > 0 ? describeDuplicateFileNames(duplicateNames) : '',
    duplicateNames.length > 0,
  );
}

export async function handleUploadClick() {
  const files = Array.from(nativeFileInput.files);

  // 処理が終わるまで、ファイル選択・アップロード・閉じるの操作をできないようにする
  selectFileBtn.disabled = true;
  uploadBtn.disabled = true;
  closeFileListBtn.disabled = true;

  // 一覧に既に同名のファイルがあるものは、アップロードせず弾く（選択時に検出済みのものを再利用する）
  const duplicateNames = getDuplicateFileNames(files);

  // 1件ずつ順番に「アップロード→テーブル作成」までまとめて行う（同時実行すると一覧更新処理が競合するため）。
  // 1件失敗しても中断せず、失敗したものだけ弾いて残りは続行する。
  // 進捗は1つのカウンタ・1つの表示エリア(.loading-status)にまとめ、内部的な段階の違いを見せない。
  const failedFiles = [];
  for (let i = 0; i < files.length; i += 1) {
    const file = files[i];

    if (duplicateNames.includes(file.name)) {
      failedFiles.push(describeDuplicateFileNames([file.name]));
      continue;
    }

    loadingStatus.textContent = `読み込み中 (${i + 1}/${files.length}): ${file.name}`;

    // ストレージにファイルをアップロードする
    const response = await uploadCsv(file);
    if (!response.ok) {
      // 失敗した場合は中断せず、このファイルの名前とエラー内容だけ記録して次に進む
      const error = await response.json();
      failedFiles.push(`${file.name}: ${error.detail}`);
      continue;
    }

    const importResponse = await importFile(file.name);
    if (!importResponse.ok) {
      const error = await importResponse.json();
      failedFiles.push(`${file.name}: ${error.detail}`);
    }
  }

  loadingStatus.textContent = '';

  // ストレージへのアップロードが失敗したファイルがあればまとめてエラー表示、なければ何も表示しない
  showStatus(
    failedFiles.length > 0 ? failedFiles.join('\n') : '',
    failedFiles.length > 0,
  );

  resetFileSelection();

  selectFileBtn.disabled = false;
  closeFileListBtn.disabled = false;
}
