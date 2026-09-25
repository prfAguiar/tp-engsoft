<template>
  <div class="dashboard-layout">
    <Navbar />
    
    <main class="dashboard-content">
      <div class="glass-card" style="text-align: center; margin-top: 40px;">
        <h2 class="title">Seu Portfólio</h2>
        <p class="subtitle">Área de integração reservada para as equipes de Investimentos e Carteira.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.dashboard-content {
  flex: 1;
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
