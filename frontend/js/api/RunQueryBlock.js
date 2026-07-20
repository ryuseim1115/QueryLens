import { apiFetch } from '../common/ApiFetch.js';

export async function runQueryBlock(queryInfo, startIndex) {
  const response = await apiFetch('/run-query-block', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...queryInfo, startIndex }),
  });
  return response;
}
