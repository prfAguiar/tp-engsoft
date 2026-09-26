<template>
  <div class="catalog-layout">
    <main class="catalog-content">
      <div class="header-section">
        <h2 class="title">Mercado Financeiro</h2>
        <p class="subtitle">Explore os investimentos disponíveis, consulte cotações em tempo real e avalie seus prazos e rentabilidades.</p>
      </div>

      <div class="glass-card catalog-card">
        <h3 class="loading-text">Carregando catálogo de investimentos...</h3>
      </div>
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.catalog-layout { display: flex; flex-direction: column; }
.catalog-content { flex: 1; padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; text-align: left; }
.title { font-size: 2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }
.catalog-card { padding: 40px !important; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; }
.loading-text { color: var(--text-main); font-weight: 400; }
</style>