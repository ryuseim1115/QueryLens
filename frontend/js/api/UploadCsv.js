export async function uploadCsv(file) {
  const formData = new FormData();
  formData.append('file', file);
  return await fetch('/upload-csv', {
    method: 'POST',
    body: formData,
  });
}
