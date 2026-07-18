import { apiFetch } from '../common/ApiFetch.js';

export async function dropTable(fileName) {
  return await apiFetch('/drop-table', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileName }),
  });
}
