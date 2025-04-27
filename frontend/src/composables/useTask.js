import { useTaskStore } from '@/stores/taskStore';

export default function useTasks() {
  const taskStore = useTaskStore();

  return {
    tasks: taskStore.tasks,
    loading: taskStore.loading,
    error: taskStore.error,
    fetchTasks: taskStore.fetchTasks,
    addTask: taskStore.addTask,
    updateTask: taskStore.updateTask,
    deleteTask: taskStore.deleteTask
  };
}