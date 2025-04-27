import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token'))
  
  const isAuthenticated = computed(() => !!token.value)

  const login = async (email, password) => {
    try {
      const response = await api.login(email, password)
      token.value = response.access_token
      localStorage.setItem('access_token', token.value)
      return true
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    token.value = null
    localStorage.removeItem('access_token')
  }

  return { token, isAuthenticated, login, logout }
})