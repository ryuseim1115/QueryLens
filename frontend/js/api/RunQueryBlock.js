import { apiFetch } from '../common/ApiFetch.js';

export async function runQueryBlock(queryInfo) {
  const response = await apiFetch('/run-query-block', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(queryInfo),
  });
  return response;
}
