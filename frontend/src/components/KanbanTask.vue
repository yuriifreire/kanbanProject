<template>
    <div
      class="kanban-task"
      :class="task.status"
      draggable="true"
      @dragstart="handleDragStart"
      @dragend="handleDragEnd"
    >
      <div class="task-header">
        <h4>{{ task.title }}</h4>
        <div class="task-actions">
          <button @click="toggleEdit" class="icon-btn" title="Editar">
            <span class="edit-icon">✏️</span>
          </button>
          <button @click="confirmDelete" class="icon-btn" title="Excluir">
            <span class="delete-icon">🗑️</span>
          </button>
        </div>
      </div>
  
      <p v-if="task.description" class="task-description">
        {{ task.description }}
      </p>
  
      <div v-if="task.due_date" class="task-due-date">
        <span class="due-icon">⏰</span>
        {{ formatDate(task.due_date) }}
      </div>
  
      <div class="task-footer">
        <span class="task-status" :style="{ backgroundColor: statusColor }">
          {{ formattedStatus }}
        </span>
        <span class="task-id">#{{ task.id }}</span>
      </div>
  
      <div v-if="isEditing" class="task-edit-modal">
        <div class="modal-content">
          <h3>Editar Tarefa</h3>
          <TaskForm
            :task="task"
            @submit="handleUpdate"
            @cancel="toggleEdit"
            mode="edit"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useTaskStore } from '@/stores/taskStore'
  import TaskForm from './TaskForm.vue'
  
  const props = defineProps({
    task: Object
  })
  
  const emit = defineEmits(['updated', 'deleted', 'dragged'])
  
  const taskStore = useTaskStore()
  const isEditing = ref(false)
  const isDragging = ref(false)
  
  const formattedStatus = computed(() => {
    const statusMap = {
      todo: 'A Fazer',
      in_progress: 'Em Progresso',
      done: 'Concluído'
    }
    return statusMap[props.task.status] || props.task.status
  })
  
  const statusColor = computed(() => {
    const colors = {
      todo: 'var(--todo-color)',
      in_progress: 'var(--in-progress-color)',
      done: 'var(--done-color)'
    }
    return colors[props.task.status] || 'var(--color-primary)'
  })
  
  const toggleEdit = () => {
    isEditing.value = !isEditing.value
  }
  
  const handleUpdate = async (updatedTask) => {
    try {
      await taskStore.updateTask(props.task.id, updatedTask)
      emit('updated')
      isEditing.value = false
    } catch (error) {
      console.error('Error updating task:', error)
    }
  }
  
  const confirmDelete = () => {
    if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
      deleteTask()
    }
  }
  
  const deleteTask = async () => {
    try {
      await taskStore.removeTask(props.task.id)
      emit('deleted')
    } catch (error) {
      console.error('Error deleting task:', error)
    }
  }
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR')
  }
  
  const handleDragStart = (e) => {
    isDragging.value = true
    e.dataTransfer.setData('taskId', props.task.id)
    emit('dragged', props.task.id)
  }
  
  const handleDragEnd = () => {
    isDragging.value = false
  }
  </script>
  
  <style scoped>
  .kanban-task {
    background-color: var(--color-card);
    border-radius: var(--radius-sm);
    padding: 12px;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
    cursor: grab;
    border-left: 3px solid v-bind(statusColor);
  }
  
  .kanban-task:active {
    cursor: grabbing;
  }
  
  .kanban-task.dragging {
    opacity: 0.5;
    transform: scale(0.98);
  }
  
  .task-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 8px;
  }
  
  .task-header h4 {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text);
    flex: 1;
  }
  
  .task-actions {
    display: flex;
    gap: 4px;
  }
  
  .icon-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    font-size: 0.9rem;
    opacity: 0.7;
    transition: opacity 0.2s;
  }
  
  .icon-btn:hover {
    opacity: 1;
  }
  
  .task-description {
    font-size: 0.9rem;
    color: var(--color-text-light);
    margin-bottom: 8px;
    white-space: pre-wrap;
  }
  
  .task-due-date {
    font-size: 0.8rem;
    color: var(--color-warning);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .task-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    font-size: 0.8rem;
  }
  
  .task-status {
    padding: 2px 8px;
    border-radius: 10px;
    color: white;
    font-weight: 500;
  }
  
  .task-id {
    color: var(--color-text-light);
    font-family: monospace;
  }
  
  .task-edit-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: var(--radius-md);
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .modal-content h3 {
    margin-bottom: 15px;
    color: var(--color-text);
  }
  </style>