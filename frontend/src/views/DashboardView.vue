<template>
  <div class="dashboard-layout">
    <main class="dashboard-content">
      <div class="header-section">
        <h2 class="title">Seu Portfólio de Investimentos</h2>
        <p class="subtitle">Visão geral do seu patrimônio e rentabilidade projetada.</p>
      </div>
      
      <div class="stats-grid">
        <div class="stat-card glass-card">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <span class="stat-label">Saldo Total</span>
            <span class="stat-value">R$ 24.500,00</span>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <span class="stat-label">Rentabilidade Acumulada</span>
            <span class="stat-value positive">+ 12,4%</span>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon">🎯</div>
          <div class="stat-info">
            <span class="stat-label">Perfil de Investidor</span>
            <span class="stat-value">Moderado</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
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
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 20px;
}
.stat-icon {
  font-size: 2.5rem;
}
.stat-info {
  display: flex;
  flex-direction: column;
}
</style>
