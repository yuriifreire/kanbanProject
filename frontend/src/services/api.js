import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor para adicionar token de autenticação
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// Response interceptor para tratar erros globais
api.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        // Token expirado ou inválido
        localStorage.removeItem('access_token')
        window.location.href = '/login'
        break
      case 403:
        // Acesso negado
        alert('Você não tem permissão para esta ação')
        break
      case 404:
        // Recurso não encontrado
        console.error('Recurso não encontrado:', error.config.url)
        break
      case 500:
        // Erro interno do servidor
        console.error('Erro interno do servidor:', error.response.data)
        break
    }
  }
  return Promise.reject(error)
})

export default {
  // Autenticação
  async login(credentials) {
    const response = await api.post('/token', credentials)
    return response.data
  },

  async refreshToken() {
    const response = await api.post('/token/refresh')
    return response.data
  },

  async logout() {
    await api.post('/token/revoke')
  },

  // Tarefas
  async getTasks() {
    const response = await api.get('/tasks/')
    return response.data
  },

  async getTask(id) {
    const response = await api.get(`/tasks/${id}`)
    return response.data
  },

  async createTask(task) {
    const response = await api.post('/tasks/', task)
    return response.data
  },

  async updateTask(id, task) {
    const response = await api.put(`/tasks/${id}`, task)
    return response.data
  },

  async deleteTask(id) {
    const response = await api.delete(`/tasks/${id}`)
    return response.data
  },

  // Upload de arquivos (se necessário)
  async uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  }
}