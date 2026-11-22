export async function getOrganizations() {
  await new Promise((r) => setTimeout(r, 500))
  return [
    { id: 1, name: 'Университет' },
    { id: 2, name: 'Компания А' },
    { id: 3, name: 'Компания Б' },
  ]
}
