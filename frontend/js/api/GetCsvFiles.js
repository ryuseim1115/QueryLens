export async function getCsvFiles() {
  const response = await fetch('/get-csv-files');
  return response.json();
}
