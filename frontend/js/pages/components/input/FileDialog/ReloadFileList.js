import { getFileTableStatus } from '../../../../api/GetFileTableStatus.js';
import { clearFileList, appendFileRow } from './FileListView.js';
import { createTables } from './CreateTables.js';

const loadingStatus = document.querySelector('.loading-status');

export async function reloadFileList() {
  loadingStatus.textContent = '読み込み中...';

  // ディスク上の全ファイルを、テーブル化済みかどうかを取得する
  const response = await getFileTableStatus();
  if (!response.ok) {
    loadingStatus.textContent = '';
    return;
  }

  const fileData = await response.json();

  // 一覧を空にしてから、既にテーブル化済みのファイルをそのまま表示する
  clearFileList();
  fileData.tabled_files.forEach((fileName) => appendFileRow(fileName));

  // 未テーブル化のファイルは、1件ずつテーブルを作成しながら一覧に追加していく
  await createTables(fileData.untabled_files);

  loadingStatus.textContent = '';
}
