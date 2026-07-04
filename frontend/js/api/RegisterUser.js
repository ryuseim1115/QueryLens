export async function registerUser(registerInfo) {
  const response = await fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registerInfo),
  });
  return response;
}
