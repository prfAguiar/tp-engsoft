<template>
  <div class="wallet-layout">
    <main class="wallet-content">
      <div class="header-section">
        <h2 class="title">Gerenciamento da Carteira</h2>
        <p class="subtitle">Administre seus aportes e acompanhe seu patrimônio.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.wallet-layout {
  display: flex;
  flex-direction: column;
}

.wallet-content {
  flex: 1;
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.header-section { margin-bottom: 40px; }

.title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--gold-accent);
}

.subtitle { color: var(--text-muted); font-size: 1.1rem; }
</style>
