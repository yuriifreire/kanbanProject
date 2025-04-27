<template>
    <form @submit.prevent="handleSubmit" class="task-form">
      <div class="form-group">
        <label for="title">Título *</label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          required
          placeholder="Digite o título da tarefa"
        />
      </div>
  
      <div class="form-group">
        <label for="description">Descrição</label>
        <textarea
          id="description"
          v-model="formData.description"
          placeholder="Digite a descrição da tarefa"
          rows="3"
        ></textarea>
      </div>
  
      <div class="form-row">
        <div class="form-group">
          <label for="status">Status *</label>
          <select id="status" v-model="formData.status" required>
            <option value="todo">A Fazer</option>
            <option value="in_progress">Em Progresso</option>
            <option value="done">Concluído</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="due_date">Data de Vencimento</label>
          <input
            id="due_date"
            v-model="formData.due_date"
            type="date"
          />
        </div>
      </div>
  
      <div class="form-actions">
        <button type="button" @click="handleCancel" class="cancel-btn" v-if="mode === 'edit'">
          Cancelar
        </button>
        <button type="submit" class="submit-btn">
          {{ mode === 'edit' ? 'Atualizar Tarefa' : 'Adicionar Tarefa' }}
        </button>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  
  const props = defineProps({
    task: {
      type: Object,
      default: null
    },
    mode: {
      type: String,
      default: 'create',
      validator: (value) => ['create', 'edit'].includes(value)
    }
  })
  
  const emit = defineEmits(['submit', 'cancel'])
  
  const formData = ref({
    title: '',
    description: '',
    status: 'todo',
    due_date: ''
  })
  
  // Preenche o formulário se estiver no modo de edição
  watch(() => props.task, (newTask) => {
    if (newTask && props.mode === 'edit') {
      formData.value = {
        title: newTask.title,
        description: newTask.description || '',
        status: newTask.status,
        due_date: newTask.due_date || ''
      }
    }
  }, { immediate: true })
  
  // Formata a data para o input date
  onMounted(() => {
    if (props.mode === 'edit' && props.task?.due_date) {
      const date = new Date(props.task.due_date)
      formData.value.due_date = date.toISOString().split('T')[0]
    }
  })
  
  const handleSubmit = () => {
    emit('submit', {
      ...formData.value,
      due_date: formData.value.due_date || null
    })
    
    if (props.mode === 'create') {
      resetForm()
    }
  }
  
  const handleCancel = () => {
    emit('cancel')
  }
  
  const resetForm = () => {
    formData.value = {
      title: '',
      description: '',
      status: 'todo',
      due_date: ''
    }
  }
  </script>
  
  <style scoped>
  .task-form {
    background-color: var(--color-card);
    padding: 20px;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: var(--color-text);
  }
  
  .form-group input,
  .form-group textarea,
  .form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    font-size: 1rem;
  }
  
  .form-group textarea {
    min-height: 80px;
    resize: vertical;
  }
  
  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }
  
  .submit-btn {
    padding: 10px 20px;
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .submit-btn:hover {
    background-color: var(--color-primary-dark);
  }
  
  .cancel-btn {
    padding: 10px 20px;
    background-color: var(--color-danger);
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: background-color 0.2s;
  }
  
  .cancel-btn:hover {
    background-color: var(--color-danger-dark);
  }
  
  @media (max-width: 768px) {
    .form-row {
      grid-template-columns: 1fr;
    }
  }
  </style>