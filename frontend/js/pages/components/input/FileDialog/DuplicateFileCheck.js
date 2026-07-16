import { getFileNames } from './FileListView.js';

// 選択されたファイルのうち、一覧に既に同名のファイルがあるものだけを名前で抽出する
export function getDuplicateFileNames(files) {
  const existingFileNames = getFileNames();
  return files
    .map((file) => file.name)
    .filter((name) => existingFileNames.includes(name));
}

// 重複しているファイル名を、エラーメッセージの文言に組み立てる
export function describeDuplicateFileNames(duplicateNames) {
  return duplicateNames
    .map((name) => `${name}: 同名のファイルが既に存在します`)
    .join('\n');
}
