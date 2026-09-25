<template>
  <nav class="premium-navbar">
    <div class="nav-brand">FinLess <span>Premium</span></div>
    <div class="nav-actions">
      <span class="user-greeting">Olá, {{ userEmail }}</span>
      <button @click="logout" class="nav-logout">Sair</button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const router = useRouter()

const userEmail = computed(() => {
  return authStore.user?.email || 'Investidor'
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.premium-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 40px;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-glass);
}
.nav-brand {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--text-main);
}
.nav-brand span {
  color: var(--gold-accent);
  font-weight: 400;
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}
.user-greeting {
  font-size: 0.95rem;
  color: var(--text-muted);
}
.nav-logout {
  background: transparent;
  border: 1px solid var(--gold-accent);
  color: var(--gold-accent);
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}
.nav-logout:hover {
  background: var(--gold-accent);
  color: #000;
}
</style>
