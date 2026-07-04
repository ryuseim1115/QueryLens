export async function authUser(authInfo) {
  const response = await fetch('/auth', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(authInfo),
  });
  return response;
}
