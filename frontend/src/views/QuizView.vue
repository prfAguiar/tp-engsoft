<template>
  <div class="quiz-layout">
    <main class="quiz-content">
      <div class="header-section">
        <h2 class="title">Descubra seu Perfil de Investidor</h2>
        <p class="subtitle">Responda a um rápido questionário para descobrirmos a melhor estratégia para você.</p>
      </div>

      <div class="glass-card quiz-card">
        <h3 class="loading-text">Carregando questionário...</h3>
      </div>
    </main>
  </div>
</template>

<script setup>
</script>

<style scoped>
.quiz-layout {
  display: flex;
  flex-direction: column;
}

.quiz-content {
  flex: 1;
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.header-section { margin-bottom: 40px; text-align: center; }

.title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--gold-accent);
}

.subtitle { color: var(--text-muted); font-size: 1.1rem; }

.quiz-card {
  padding: 40px !important;
  text-align: center;
}

.loading-text {
  color: var(--text-main);
  font-weight: 400;
}
</style>
