export async function apiFetch(url, options) {
  const response = await fetch(url, options);
  if (response.status === 401) {
    location.href = '/login';
  }
  return response;
}
