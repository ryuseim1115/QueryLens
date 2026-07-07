export async function deleteCsv(fileName) {
  return await fetch('/delete-csv-file', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileName }),
  });
}
