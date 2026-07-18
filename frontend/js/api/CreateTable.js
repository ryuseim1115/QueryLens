import { apiFetch } from '../common/ApiFetch.js';

export async function createTable(fileName) {
  return await apiFetch('/create-table', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fileName }),
  });
}
