<template>
  <div class="register-container">
    <h2>Cadastro FinLess</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label>Nome (opcional):</label>
        <input type="text" v-model="firstName" />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div>
        <label>Senha:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Criar Conta</button>
      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    </form>
    <router-link to="/login">Já possui conta? Entre aqui.</router-link>
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
.error { color: red; }
</style>
