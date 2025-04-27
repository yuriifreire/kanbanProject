import { defineStore } from 'pinia'
import api from '@/services/api'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    tasks: [],
    loading: false,
    error: null,
    currentTask: null
  }),

  actions: {
    async fetchTasks() {
      this.loading = true
      this.error = null
      try {
        const response = await api.getTasks()
        this.tasks = response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Falha ao carregar tarefas'
        console.error('Error fetching tasks:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchTask(id) {
      this.loading = true
      this.error = null
      try {
        const response = await api.getTask(id)
        this.currentTask = response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Falha ao carregar tarefa'
        console.error('Error fetching task:', error)
      } finally {
        this.loading = false
      }
    },

    async addTask(task) {
      this.loading = true
      this.error = null
      try {
        const response = await api.createTask(task)
        this.tasks.push(response)
        return response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Falha ao criar tarefa'
        console.error('Error creating task:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateTask(id, task) {
      this.loading = true
      this.error = null
      try {
        const response = await api.updateTask(id, task)
        const index = this.tasks.findIndex(t => t.id === id)
        if (index !== -1) {
          this.tasks[index] = response
        }
        return response
      } catch (error) {
        this.error = error.response?.data?.detail || 'Falha ao atualizar tarefa'
        console.error('Error updating task:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async removeTask(id) {
      this.loading = true
      this.error = null
      try {
        await api.deleteTask(id)
        this.tasks = this.tasks.filter(task => task.id !== id)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Falha ao remover tarefa'
        console.error('Error deleting task:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  },

  getters: {
    todoTasks: (state) => state.tasks.filter(task => task.status === 'todo'),
    inProgressTasks: (state) => state.tasks.filter(task => task.status === 'in_progress'),
    doneTasks: (state) => state.tasks.filter(task => task.status === 'done'),
    getTaskById: (state) => (id) => state.tasks.find(task => task.id === id)
  }
})