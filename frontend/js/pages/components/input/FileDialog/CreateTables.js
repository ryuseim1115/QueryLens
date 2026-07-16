import { createTable } from '../../../../api/CreateTable.js';
import { appendFileRow } from './FileListView.js';

const loadingStatus = document.querySelector('.loading-status');

// サーバーにテーブル作成を依頼し、成功した場合のみその1件を一覧に追加する
export async function importFile(fileName) {
  const response = await createTable(fileName);
  if (response.ok) {
    appendFileRow(fileName);
  }
  return response;
}

// 渡されたファイル名の分だけ、1件ずつ順番にインメモリへテーブルを作成する
export async function createTables(fileNames) {
  const total = fileNames.length;

  for (let i = 0; i < total; i += 1) {
    const fileName = fileNames[i];

    // 進捗（何件中の何件目か）をローディング表示に反映する
    loadingStatus.textContent = `読み込み中 (${i + 1}/${total}): ${fileName}`;

    // 作成が完了した時点で、その1件だけ一覧に追加する（全件完了を待たずに順次表示する）
    await importFile(fileName);
  }
}
