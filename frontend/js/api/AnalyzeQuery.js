import { apiFetch } from '../common/ApiFetch.js';

export async function analyzeQuery(queryInfo) {
  const response = await apiFetch('/analyze-query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(queryInfo),
  });
  return response;
}
