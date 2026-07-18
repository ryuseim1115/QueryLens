import { apiFetch } from '../common/ApiFetch.js';

export async function runQuery(queryInfo) {
  const response = await apiFetch('/run-query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(queryInfo),
  });
  return response;
}
