const base = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const token = {
  get: () => localStorage.getItem('vorbis_token'),
  set: (value: string) => localStorage.setItem('vorbis_token', value),
  clear: () => localStorage.removeItem('vorbis_token'),
}
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (token.get()) headers.set('Authorization', `Bearer ${token.get()}`)
  if (init.body && !(init.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  const response = await fetch(`${base}${path}`, { ...init, headers })
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || response.statusText)
  return response.status === 204 ? undefined as T : response.json()
}
