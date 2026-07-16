import { apiFetch } from '../common/ApiFetch.js';

export async function purgeFile(fileName) {
  return await apiFetch('/purge-file', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileName }),
  });
}
