// クエリ文字列を行ごとに分割し、各行の元クエリ内でのオフセットを記録する
// 例: splitLinesWithOffsets("SELECT * FROM (\nSELECT id FROM users\n) AS u") は
//   [
//     { text: "SELECT * FROM (",          start_index: 0,  end_index: 15 },
//     { text: "SELECT id FROM users",     start_index: 16, end_index: 37 },
//     { text: ") AS u",                   start_index: 38, end_index: 44 },
//   ]
// を返す（start_indexは各行の先頭が元クエリ全体で何文字目かを表す。改行の分だけ+1される）
export function splitLinesWithOffsets(query) {
  const lineOffsets = [];
  let offset = 0;
  query.split('\n').forEach((text) => {
    const start_index = offset;
    const end_index = start_index + text.length;
    lineOffsets.push({ text, start_index, end_index });
    offset = end_index + 1; // +1 は改行文字の分
  });
  return lineOffsets;
}
