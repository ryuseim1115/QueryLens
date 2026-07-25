export function renderResultTable(rows) {
  const { noResultEl, thead, tbody } = resetResultBody();

  if (!rows || !rows.length) {
    noResultEl.classList.add('visible');
    return;
  }

  const columns = Object.keys(rows[0]);
  thead.appendChild(buildHeaderRow(columns));
  rows.forEach((row) => tbody.appendChild(buildDataRow(row, columns)));
}

// クエリブロック単体実行の失敗時（相関サブクエリなど）に、テーブルの代わりにエラーメッセージを表示する
export function renderResultError(message) {
  const { errorEl } = resetResultBody();
  errorEl.textContent = message;
  errorEl.classList.add('visible');
}

function resetResultBody() {
  const noResultEl = document.querySelector('.no-result');
  const errorEl = document.querySelector('.result-error');
  const thead = document.querySelector('.result-body thead');
  const tbody = document.querySelector('.result-body tbody');

  noResultEl.classList.remove('visible');
  errorEl.classList.remove('visible');
  thead.replaceChildren();
  tbody.replaceChildren();

  return { noResultEl, errorEl, thead, tbody };
}

function buildHeaderRow(columns) {
  const tr = document.createElement('tr');
  columns.forEach((col) => {
    const th = document.createElement('th');
    th.textContent = col;
    tr.appendChild(th);
  });
  return tr;
}

function buildDataRow(row, columns) {
  const tr = document.createElement('tr');
  columns.forEach((col) => {
    const td = document.createElement('td');
    td.textContent = row[col];
    tr.appendChild(td);
  });
  return tr;
}
