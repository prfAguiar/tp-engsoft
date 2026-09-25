<template>
  <div class="login-container">
    <h2>Login FinLess</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Senha:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Entrar</button>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import api from '@/services/api'

const email = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    const res = await api.post('users/login/', { email: email.value, password: password.value })
    authStore.setAuth(res.data.access, { email: email.value })
    router.push('/')
  } catch (err) {
    errorMsg.value = 'Credenciais inválidas!'
  }
}
</script>

<style scoped>
.error { color: red; }
</style>
