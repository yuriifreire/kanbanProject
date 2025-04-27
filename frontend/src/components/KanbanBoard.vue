<template>
  <div class="kanban-board">
    <h1>Kanban Board</h1>
    <TaskForm @task-created="fetchTasks" />
    
    <div v-if="loading" class="loading">Carregando tarefas...</div>
    <div v-else class="columns">
      <KanbanColumn
        v-for="column in columns"
        :key="column.status"
        :title="column.title"
        :status="column.status"
        :tasks="filteredTasks(column.status)"
        @task-updated="fetchTasks"
        @task-deleted="fetchTasks"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTaskStore } from '@/stores/taskStore'
import KanbanColumn from './KanbanColumn.vue'
import TaskForm from './TaskForm.vue'

const taskStore = useTaskStore()
const loading = ref(false)

const columns = [
  { title: 'A Fazer', status: 'todo' },
  { title: 'Em Progresso', status: 'in_progress' },
  { title: 'Concluído', status: 'done' }
]

const filteredTasks = (status) => {
  return taskStore.tasks.filter(task => task.status === status)
}

const fetchTasks = async () => {
  loading.value = true
  await taskStore.fetchTasks()
  loading.value = false
}

onMounted(() => {
  fetchTasks()
})
</script>