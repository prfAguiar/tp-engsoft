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

      <div class="charts-grid">
        <div class="chart-card glass-card">
          <h3 class="chart-title">Distribuição da Carteira</h3>
          <div class="chart-container pie-container">
            <Pie :data="pieData" :options="pieOptions" />
          </div>
        </div>
        <div class="chart-card glass-card">
          <h3 class="chart-title">Projeção de Crescimento (12 meses)</h3>
          <div class="chart-container">
            <Line :data="lineData" :options="lineOptions" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Filler } from 'chart.js';
import { Pie, Line } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement, ArcElement, Filler);

const pieData = ref({
  labels: ['Tesouro Direto', 'CDBs', 'Fundos Imobiliários', 'Ações'],
  datasets: [{ backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'], borderWidth: 0, data: [40, 25, 20, 15] }]
});

const pieOptions = ref({
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { position: 'bottom' } }
});

const lineData = ref({
  labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
  datasets: [{
    label: 'Patrimônio Projetado (R$)',
    backgroundColor: 'rgba(59, 130, 246, 0.2)', borderColor: '#3b82f6', borderWidth: 2, fill: true,
    data: [20000, 20500, 21100, 21600, 22000, 22600, 23100, 23800, 24500, 25100, 25800, 26500]
  }]
});

const lineOptions = ref({
  responsive: true, maintainAspectRatio: false,
  plugins: { legend: { display: false } }
});
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
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
}
.chart-card {
  display: flex;
  flex-direction: column;
}
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
.pie-container {
  height: 280px;
}
</style>
