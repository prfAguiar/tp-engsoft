<template>
  <div class="auth-wrapper">
    <div class="glass-card auth-card" style="text-align: center;">
      <h2 class="title">Painel Principal</h2>
      <p class="subtitle">Em breve: Gestão do seu Perfil e Carteira</p>
      <button @click="logout" class="premium-btn" style="margin-top: 20px;">Sair da Conta</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
