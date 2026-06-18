export async function dropTable(fileName) {
  return await fetch('/drop-csv-table', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileName }),
  });
}
