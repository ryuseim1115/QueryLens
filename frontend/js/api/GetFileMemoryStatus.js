import { apiFetch } from '../common/ApiFetch.js';

export async function getFileMemoryStatus() {
  return await apiFetch('/get-file-memory-status');
}
