import { purgeFile } from '../../../../api/PurgeFile.js';

// 削除ボタン(deleteBtn)に、クリックされたときの処理を登録する
export function addPurgeListener(deleteBtn, fileName) {
  deleteBtn.addEventListener('click', async () => {
    // 連打防止のためボタンを無効化し、レイアウトのズレを防ぐため非表示にする
    deleteBtn.disabled = true;
    deleteBtn.style.display = 'none';

    // ボタンの直後に「削除中...」の表示を追加する
    const loadingSpan = document.createElement('span');
    loadingSpan.textContent = '削除中...';
    deleteBtn.after(loadingSpan);

    // サーバーにインメモリ削除+ストレージ削除を依頼し、完了を待つ
    await purgeFile(fileName);

    // 完了したら、このボタンが属する行(.file-row)ごと画面から取り除く
    deleteBtn.closest('.file-row').remove();
  });
}
