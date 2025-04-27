<template>
  <header class="app-header">
    <div class="logo">
      <img src="@/assets/logo.svg" alt="Logo">
      <h1>Kanban Board</h1>
    </div>
    <button v-if="isAuthenticated" @click="logout" class="logout-btn">
      Sair
    </button>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const isAuthenticated = computed(() => authStore.isAuthenticated);

const logout = () => {
  authStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>