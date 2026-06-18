export async function createTable(fileName) {
  return await fetch('/create-csv-table', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileName }),
  });
}
