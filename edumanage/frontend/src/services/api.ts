import axios from 'axios'

const instance = axios.create({
  baseURL: '/api',
})

let authToken: string | null = null

instance.interceptors.request.use((config) => {
  if (authToken) {
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${authToken}`
  }
  return config
})

export const api = {
  setToken: (token: string | null) => { authToken = token },
  get: instance.get,
  post: instance.post,
  put: instance.put,
  delete: instance.delete,
}