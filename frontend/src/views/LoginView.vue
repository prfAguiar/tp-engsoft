<template>
  <div class="auth-wrapper">
    <div class="glass-card auth-card">
      <h2 class="title">Entrar na sua Carteira</h2>
      <p class="subtitle">Bem-vindo de volta à FinLess Premium</p>
      
      <form @submit.prevent="handleLogin" class="form-layout">
        <div class="input-group">
          <label>Endereço de Email</label>
          <input type="email" v-model="email" :class="['premium-input', { 'has-error': hasError }]" placeholder="seu@email.com" required @input="clearError" />
        </div>
        <div class="input-group">
          <label>Senha de Acesso</label>
          <input type="password" v-model="password" :class="['premium-input', { 'has-error': hasError }]" placeholder="••••••••" required @input="clearError" />
        </div>
        
        <button type="submit" class="premium-btn" :disabled="isLoading">
          {{ isLoading ? 'Acessando Cofre...' : 'Acessar Painel' }}
        </button>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      </form>
      
      <div class="auth-footer">
        Ainda não tem convite? <router-link to="/register" class="gold-link">Crie sua conta</router-link>
      </div>
    </div>
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
const hasError = ref(false)
const isLoading = ref(false)
const router = useRouter()
const authStore = useAuthStore()

const clearError = () => {
  hasError.value = false
  errorMsg.value = ''
}

const handleLogin = async () => {
  if (isLoading.value) return
  isLoading.value = true
  clearError()
  
  try {
    const res = await api.post('users/login/', { email: email.value, password: password.value })
    authStore.setAuth(res.data.access, { email: email.value })
    router.push('/')
  } catch (err) {
    hasError.value = true
    if (err.response && err.response.status === 401) {
      errorMsg.value = 'Acesso negado. Credenciais inválidas.'
    } else {
      errorMsg.value = 'Falha de comunicação com a matriz.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}
.auth-card {
  width: 100%;
  max-width: 420px;
}
.title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 5px;
}
.subtitle {
  color: var(--text-muted);
  margin-bottom: 30px;
  font-size: 0.95rem;
}
.form-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.input-group label {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-weight: 500;
}
.auth-footer {
  margin-top: 30px;
  text-align: center;
  font-size: 0.9rem;
  color: var(--text-muted);
}
.gold-link {
  color: var(--gold-accent);
  text-decoration: none;
  font-weight: 500;
}
.gold-link:hover { text-decoration: underline; }
.error-msg {
  color: #ff4a4a;
  font-size: 0.85rem;
  text-align: center;
  margin-top: -10px;
}
</style>
