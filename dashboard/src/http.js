import axios from 'axios'
import { getUser } from './auth'
const api = axios.create({ baseURL: import.meta.env.VITE_MANAGER_API || 'http://localhost:8000' })
api.interceptors.request.use(async (cfg) => {
  const u = await getUser()
  if (u && u.access_token) cfg.headers.Authorization = `Bearer ${u.access_token}`
  return cfg
})
export default api
