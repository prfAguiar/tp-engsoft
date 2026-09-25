<template>
  <div class="auth-wrapper">
    <div class="glass-card auth-card">
      <h2 class="title">Criar Conta FinLess</h2>
      <p class="subtitle">Junte-se à plataforma premium de investimentos</p>
      
      <form @submit.prevent="handleRegister" class="form-layout">
        <div class="input-group">
          <label>Como quer ser chamado?</label>
          <input type="text" v-model="firstName" class="premium-input" placeholder="Seu nome (opcional)" />
        </div>
        <div class="input-group">
          <label>Endereço de Email</label>
          <input type="email" v-model="email" class="premium-input" placeholder="seu@email.com" required />
        </div>
        <div class="input-group">
          <label>Crie uma Senha Forte</label>
          <input type="password" v-model="password" class="premium-input" placeholder="••••••••" required />
        </div>
        
        <button type="submit" class="premium-btn">Criar Conta Exclusiva</button>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      </form>
      
      <div class="auth-footer">
        Já possui acesso? <router-link to="/login" class="gold-link">Entre aqui</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const firstName = ref('')
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()

const handleRegister = async () => {
  try {
    await api.post('users/register/', { 
      email: email.value, 
      password: password.value, 
      first_name: firstName.value 
    })
    // Redireciona para o login após sucesso
    router.push('/login')
  } catch (err) {
    errorMsg.value = 'Falha ao criar conta. Tente outro email.'
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
