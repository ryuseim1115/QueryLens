import { openDialog } from './DialogControl.js';
import { reloadFileList } from './ReloadFileList.js';
import { showStatus } from './UploadFile.js';

const selectFileBtn = document.querySelector('.select-file-btn');

// 「解析対象のファイルを選択」ボタンが押されたときの処理
export async function handleOpenFileDialogClick() {
  // 前回開いたときのアップロード状況メッセージが残らないようにする
  showStatus('', false);

  // 読み込みが終わるまで「ファイルを選択」を非活性にする
  selectFileBtn.disabled = true;
  openDialog();

  // サーバー側の最新状態を取得し、一覧に反映する
  await reloadFileList();

  selectFileBtn.disabled = false;
}
