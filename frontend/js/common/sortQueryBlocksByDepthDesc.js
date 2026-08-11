// queryBlocksをdepthの降順（ネストが深い順）に並べ替える
// TableListController.js・DisplayLines.js・ResultPopupListener.jsは、
// この並び順を前提に配列の位置だけでルートブロック（depth0）を判定している
export function sortQueryBlocksByDepthDesc(queryBlocks) {
  return [...queryBlocks].sort((a, b) => b.depth - a.depth);
}
