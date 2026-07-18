import { apiFetch } from '../common/ApiFetch.js';

export async function getFileTableStatus() {
  return await apiFetch('/get-file-table-status');
}
