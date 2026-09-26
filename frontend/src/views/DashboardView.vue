<template>
  <div class="dashboard-layout">
    <main class="dashboard-content">
      <div class="header-section">
        <h2 class="title">Seu Portfólio de Investimentos</h2>
        <p class="subtitle">Visão geral do seu patrimônio e rentabilidade projetada.</p>
      </div>
      
      <div class="stats-grid">
        <div class="stat-card glass-card custom-padding">
          <div class="stat-icon">💰</div>
          <div class="stat-info">
            <span class="stat-label">Saldo Total</span>
            <span class="stat-value">R$ 24.500,00</span>
          </div>
        </div>
        <div class="stat-card glass-card custom-padding">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <span class="stat-label">Rentabilidade Acumulada</span>
            <span class="stat-value positive">+ 12,4%</span>
          </div>
        </div>
        <div class="stat-card glass-card custom-padding">
          <div class="stat-icon">🎯</div>
          <div class="stat-info">
            <span class="stat-label">Perfil de Investidor</span>
            <span class="stat-value">Moderado</span>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card glass-card custom-padding">
          <h3 class="chart-title">Distribuição da Carteira</h3>
          <div class="chart-container pie-container">
            <Pie :data="pieData" :options="pieOptions" />
          </div>
        </div>
        <div class="chart-card glass-card custom-padding">
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
  datasets: [{ 
    backgroundColor: ['#d4af37', '#475569', '#e2e8f0', '#b45309'], 
    borderWidth: 0, 
    data: [40, 25, 20, 15] 
  }]
});

const pieOptions = ref({
  responsive: true, maintainAspectRatio: false,
  plugins: { 
    legend: { position: 'bottom', labels: { color: '#f5f5f7', padding: 20, font: { family: "'Outfit', sans-serif", size: 13 } } },
    tooltip: { backgroundColor: 'rgba(9, 10, 15, 0.9)', padding: 12, cornerRadius: 8 }
  }
});

const lineData = ref({
  labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
  datasets: [{
    label: 'Patrimônio Projetado (R$)',
    backgroundColor: 'rgba(212, 175, 55, 0.15)', borderColor: '#d4af37', borderWidth: 2, 
    pointBackgroundColor: '#d4af37', pointBorderColor: '#fff', pointHoverBackgroundColor: '#fff', pointHoverBorderColor: '#d4af37',
    fill: true, data: [20000, 20500, 21100, 21600, 22000, 22600, 23100, 23800, 24500, 25100, 25800, 26500]
  }]
});

const lineOptions = ref({
  responsive: true, maintainAspectRatio: false,
  scales: {
    y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#8a8d98', font: { family: "'Outfit', sans-serif" } } },
    x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#8a8d98', font: { family: "'Outfit', sans-serif" } } }
  },
  plugins: { legend: { display: false }, tooltip: { backgroundColor: 'rgba(9, 10, 15, 0.9)', padding: 12, cornerRadius: 8 } }
});
</script>

<style scoped>
.dashboard-layout {
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

.header-section { margin-bottom: 40px; }

.title {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--gold-accent);
}

.subtitle { color: var(--text-muted); font-size: 1.1rem; }

.custom-padding {
  padding: 24px !important;
}

.glass-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px var(--gold-glow);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.stat-card { display: flex; align-items: center; gap: 20px; }

.stat-icon {
  font-size: 2.5rem;
  background: var(--border-glass);
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.stat-info { display: flex; flex-direction: column; }
.stat-label { color: var(--text-muted); font-size: 0.9rem; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 1.5rem; font-weight: 600; color: var(--text-main); }
.stat-value.positive { color: #10b981; }

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 24px;
}

.chart-card { display: flex; flex-direction: column; }
.chart-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 20px; color: var(--text-main); }
.chart-container { position: relative; height: 300px; width: 100%; }
.pie-container { height: 280px; }

@media (max-width: 768px) {
  .charts-grid { grid-template-columns: 1fr; }
}
</style>

