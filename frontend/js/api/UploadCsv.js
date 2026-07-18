import { apiFetch } from '../common/ApiFetch.js';

export async function uploadCsv(file) {
  const formData = new FormData();
  formData.append('file', file);
  return await apiFetch('/upload-csv', {
    method: 'POST',
    body: formData,
  });
}
