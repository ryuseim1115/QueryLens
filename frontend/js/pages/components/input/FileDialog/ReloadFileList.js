import { getFileMemoryStatus } from '../../../../api/GetFileMemoryStatus.js';
import { clearFileList, appendFileRow } from './FileListView.js';
import { createTables } from './CreateTables.js';

const loadingStatus = document.querySelector('.loading-status');

export async function reloadFileList() {
  loadingStatus.textContent = '読み込み中...';

  // ストレージ上の全ファイルを、インメモリに存在するかどうかを取得する
  const response = await getFileMemoryStatus();
  if (!response.ok) {
    loadingStatus.textContent = '';
    return;
  }

  const fileData = await response.json();

  // 一覧を空にしてから、既にインメモリにあるファイルをそのまま表示する
  clearFileList();
  fileData.in_memory_files.forEach((fileName) => appendFileRow(fileName));

  // インメモリにまだないファイルは、1件ずつインメモリにテーブルを作成しながら一覧に追加していく
  await createTables(fileData.not_in_memory_files);

  loadingStatus.textContent = '';
}
