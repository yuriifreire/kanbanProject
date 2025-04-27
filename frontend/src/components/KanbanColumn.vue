<template>
  <div 
    class="kanban-column"
    :style="{ '--column-color': color }"
    @dragover.prevent="handleDragOver"
    @drop="handleDrop"
  >
    <div class="column-header">
      <h3 :style="{ color: color }">{{ title }}</h3>
      <span class="task-count">{{ filteredTasks.length }}</span>
    </div>

    <div 
      class="tasks-container"
      :class="{ 'empty-column': filteredTasks.length === 0 }"
    >
      <KanbanTask
        v-for="task in filteredTasks"
        :key="task.id"
        :task="task"
        @updated="$emit('task-updated')"
        @deleted="$emit('task-deleted')"
        @dragged="handleTaskDrag"
      />

      <div v-if="filteredTasks.length === 0" class="empty-state">
        Nenhuma tarefa nesta coluna
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import KanbanTask from './KanbanTask.vue'

const props = defineProps({
  title: String,
  status: String,
  color: {
    type: String,
    default: 'var(--color-primary)'
  },
  tasks: Array
})

const emit = defineEmits(['task-updated', 'task-deleted', 'task-moved'])

const filteredTasks = computed(() => {
  return props.tasks.filter(task => task.status === props.status)
})

const handleTaskDrag = (taskId) => {
  // Pode ser usado para feedback visual durante o drag
}

const handleDragOver = (e) => {
  e.preventDefault()
  e.dataTransfer.dropEffect = 'move'
}

const handleDrop = (e) => {
  e.preventDefault()
  const taskId = e.dataTransfer.getData('taskId')
  if (taskId) {
    emit('task-moved', taskId, props.status)
  }
}
</script>

<style scoped>
.kanban-column {
  background-color: var(--color-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  padding: 15px;
  min-height: 300px;
  display: flex;
  flex-direction: column;
}

.column-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 10px;
  margin-bottom: 15px;
  border-bottom: 2px solid var(--color-border);
}

.column-header h3 {
  font-size: 1.2rem;
  font-weight: 600;
}

.task-count {
  background-color: var(--column-color, var(--color-primary));
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.tasks-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  padding: 5px;
}

.tasks-container.empty-column {
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: var(--radius-sm);
  justify-content: center;
  align-items: center;
}

.empty-state {
  color: var(--color-text-light);
  font-size: 0.9rem;
  text-align: center;
  padding: 20px;
}
</style>