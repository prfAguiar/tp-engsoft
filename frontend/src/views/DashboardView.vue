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
            <span class="stat-value">{{ totalBalance.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) }}</span>
          </div>
        </div>
        <div class="stat-card glass-card custom-padding">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <span class="stat-label">Rentabilidade Projetada</span>
            <span class="stat-value positive">{{ accumulatedProfitability }}</span>
          </div>
        </div>
        <div class="stat-card glass-card custom-padding">
          <div class="stat-icon">🎯</div>
          <div class="stat-info">
            <span class="stat-label">Perfil de Investidor</span>
            <span class="stat-value">{{ investorProfile }}</span>
          </div>
        </div>
      </div>

      <div class="charts-grid">
        <div class="chart-card glass-card custom-padding">
          <h3 class="chart-title">Distribuição da Carteira</h3>
          <div class="chart-container pie-container">
            <Pie :data="pieData" :options="pieOptions" v-if="loaded" />
          </div>
        </div>
        <div class="chart-card glass-card custom-padding">
          <h3 class="chart-title">Projeção de Crescimento (12 meses)</h3>
          <div class="chart-container">
            <Line :data="lineData" :options="lineOptions" v-if="loaded" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Filler } from 'chart.js';
import { Pie, Line } from 'vue-chartjs';
import api from '@/services/api';
import { useAuthStore } from '@/store/auth';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement, ArcElement, Filler);

const authStore = useAuthStore();
const totalBalance = ref(0);
const profileMap = {
  'CONSERVATIVE': 'Conservador',
  'MODERATE': 'Moderado',
  'AGGRESSIVE': 'Arrojado'
};
const investorProfile = computed(() => {
  const p = authStore.user?.investor_profile;
  return profileMap[p] || p || 'Não definido';
});
const accumulatedProfitability = ref('...');
const loaded = ref(false);

const pieData = ref({ labels: [], datasets: [] });
const lineData = ref({ labels: [], datasets: [] });

const pieOptions = ref({
  responsive: true, maintainAspectRatio: false,
  plugins: { 
    legend: { position: 'bottom', labels: { color: '#f5f5f7', padding: 20, font: { family: "'Outfit', sans-serif", size: 13 } } },
    tooltip: { backgroundColor: 'rgba(9, 10, 15, 0.9)', padding: 12, cornerRadius: 8 }
  }
});

const lineOptions = ref({
  responsive: true, maintainAspectRatio: false,
  scales: {
    y: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#8a8d98', font: { family: "'Outfit', sans-serif" } } },
    x: { grid: { color: 'rgba(255, 255, 255, 0.05)' }, ticks: { color: '#8a8d98', font: { family: "'Outfit', sans-serif" } } }
  },
  plugins: { legend: { display: false }, tooltip: { backgroundColor: 'rgba(9, 10, 15, 0.9)', padding: 12, cornerRadius: 8 } }
});

const fetchDashboardData = async () => {
  try {
    const walletRes = await api.get('wallets/');
    const wallet = walletRes.data;
    totalBalance.value = parseFloat(wallet.total_amount) || 0;
    
    const typesMap = {};
    if (wallet.items && wallet.items.length > 0) {
      wallet.items.forEach(item => {
        const type = item.investment_type;
        typesMap[type] = (typesMap[type] || 0) + parseFloat(item.amount);
      });
    }
    
    const labels = Object.keys(typesMap).length ? Object.keys(typesMap) : ['Sem ativos'];
    const data = Object.values(typesMap).length ? Object.values(typesMap) : [1];
    
    pieData.value = {
      labels: labels,
      datasets: [{ backgroundColor: ['#d4af37', '#475569', '#e2e8f0', '#b45309'], borderWidth: 0, data: data }]
    };

    const projRes = await api.post('investments/projection/', {
      initial_amount: totalBalance.value || 1000,
      monthly_contribution: 0,
      annual_rate: 10.5,
      period_months: 12
    });
    
    const projData = projRes.data;
    if (projData && projData.evolution) {
      lineData.value = {
        labels: projData.evolution.map(p => "Mês " + p.month),
        datasets: [{
          label: 'Patrimônio Projetado (R$)',
          backgroundColor: 'rgba(212, 175, 55, 0.15)', borderColor: '#d4af37', borderWidth: 2, 
          pointBackgroundColor: '#d4af37', pointBorderColor: '#fff',
          fill: true, data: projData.evolution.map(p => p.total_balance)
        }]
      };
      
      const profitPercent = totalBalance.value > 0 ? (projData.total_interest_earned / totalBalance.value) * 100 : 10.5;
      accumulatedProfitability.value = "+ " + profitPercent.toFixed(1) + "% (Proj. 12m)";
    }
    loaded.value = true;
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
};

onMounted(() => { fetchDashboardData(); });
</script>

<style scoped>
.dashboard-layout { display: flex; flex-direction: column; }
.dashboard-content { flex: 1; padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; }
.title { font-size: 2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }
.custom-padding { padding: 24px !important; }
.glass-card:hover { transform: translateY(-2px); box-shadow: 0 10px 30px var(--gold-glow); }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 40px; }
.stat-card { display: flex; align-items: center; gap: 20px; }
.stat-icon { font-size: 2.5rem; background: var(--border-glass); width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; border-radius: 12px; }
.stat-info { display: flex; flex-direction: column; }
.stat-label { color: var(--text-muted); font-size: 0.9rem; font-weight: 500; margin-bottom: 4px; }
.stat-value { font-size: 1.5rem; font-weight: 600; color: var(--text-main); }
.stat-value.positive { color: #10b981; }
.charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 24px; }
.chart-card { display: flex; flex-direction: column; }
.chart-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 20px; color: var(--text-main); }
.chart-container { position: relative; height: 300px; width: 100%; }
.pie-container { height: 280px; }
@media (max-width: 768px) { .charts-grid { grid-template-columns: 1fr; } }
</style>


