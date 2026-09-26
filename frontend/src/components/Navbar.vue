<template>
  <nav class="premium-navbar">
    <router-link to="/" class="nav-brand">
      <img src="@/assets/logotipo_nomeempresa.png" alt="FinLess Logo" class="brand-logo" />
    </router-link>
    
    <div class="nav-links" v-if="authStore.isAuthenticated">
      <router-link to="/" class="nav-link">Dashboard</router-link>
      <router-link to="/wallet" class="nav-link">Minha Carteira</router-link>
      <router-link to="/catalog" class="nav-link">Mercado</router-link>
      <router-link to="/suggestion" class="nav-link">Sugestões</router-link>
      <router-link to="/quiz" class="nav-link">Descobrir Perfil</router-link>
    </div>

    <div class="nav-actions" v-if="authStore.isAuthenticated">
      <span class="user-greeting">Olá, {{ userDisplayName }}</span>
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

const userDisplayName = computed(() => {
  return authStore.user?.first_name || authStore.user?.email || 'Investidor'
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.premium-navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 30px; /* Adicionado espaço vertical (respiro) */
  min-height: 85px;
  height: auto;
  box-sizing: border-box;
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-glass);
}
.nav-brand {
  display: flex;
  align-items: center;
  text-decoration: none;
}
.brand-logo {
  height: 100px; /* Tamanho equilibrado sem exagero */
  width: auto;
  object-fit: contain;
}
.nav-brand span {
  color: var(--gold-accent);
  font-weight: 400;
}
.nav-links {
  display: flex;
  
}
.nav-link { color: var(--text-muted); text-decoration: none; font-weight: 500; font-size: 1rem; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); display: inline-block; padding: 10px 15px; }

.nav-link.router-link-active { color: var(--gold-accent); font-size: 1.3rem; }

.nav-links:hover .nav-link.router-link-active { font-size: 1rem; }

.nav-link:hover { color: #ffffff !important; font-size: 1.3rem !important; }

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

