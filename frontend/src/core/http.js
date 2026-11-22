import { API_URL } from './config'

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message)
    this.status = status
    this.data = data
  }
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json' }
  const token = localStorage.getItem('access_token')
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(API_URL + path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  })

  const data = res.status === 204 ? null : await res.json().catch(() => null)
  if (!res.ok) {
    const message = typeof data?.detail === 'string' ? data.detail : 'Ошибка запроса'
    throw new ApiError(message, res.status, data)
  }
  return data
}

export const http = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body ?? {}),
  put: (path, body) => request('PUT', path, body),
  patch: (path, body) => request('PATCH', path, body),
  delete: (path) => request('DELETE', path),
}
