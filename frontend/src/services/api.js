import axios from 'axios'

const API_PATH = '/api'
const api = axios.create({
  baseURL: API_PATH,
  headers: { 'Content-Type': 'multipart/form-data' },
})

export const getFileUrl = (path) => {
  if (!path) return '#'
  if (path.startsWith('http')) return path

  const cleanPath = path.replace(/^\/+/, '')
  return `/${cleanPath}`
}

export default api
