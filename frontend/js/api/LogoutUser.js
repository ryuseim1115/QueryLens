export async function logoutUser() {
  const response = await fetch('/logout', {
    method: 'POST',
  });
  return response;
}
