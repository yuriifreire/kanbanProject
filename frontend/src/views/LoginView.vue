<template>
  <div class="login-view">
    <form @submit.prevent="handleLogin">
      <h2>Login</h2>
      <input v-model="email" type="email" placeholder="Email" required>
      <input v-model="password" type="password" placeholder="Senha" required>
      <button type="submit">Entrar</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref(null);
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    await authStore.login(email.value, password.value);
    router.push('/');
  } catch (err) {
    error.value = 'Credenciais inválidas';
  }
};
</script>