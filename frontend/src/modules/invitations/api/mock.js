export async function registerByInvite(token, data) {
  await new Promise((r) => setTimeout(r, 700))
  if (data.login === 'admin') {
    throw new Error('Такой логин уже занят')
  }
  console.log('Отправили:', token, data)
}
