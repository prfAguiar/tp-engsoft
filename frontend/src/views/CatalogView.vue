<template>
  <div class="catalog-layout">
    <main class="catalog-content">
      <div class="header-section">
        <h2 class="title">Mercado Financeiro</h2>
        <p class="subtitle">Explore os investimentos disponíveis, consulte cotações em tempo real e avalie seus prazos e rentabilidades.</p>
      </div>

      <div class="glass-card catalog-card" v-if="loading">
        <h3 class="loading-text">Carregando catálogo de investimentos...</h3>
      </div>

      <div class="catalog-grid" v-else-if="assets.length > 0">
        <div class="glass-card asset-card" v-for="asset in assets" :key="asset.id">
          <div class="asset-header">
            <h3 class="asset-name">{{ asset.name }}</h3>
            <span class="asset-ticker" v-if="asset.ticker">{{ asset.ticker }}</span>
          </div>
          
          <div class="asset-tags">
            <span class="tag type-tag">{{ formatType(asset.type) }}</span>
            <span class="tag risk-tag" :class="asset.risk_level.toLowerCase()">Risco {{ formatRisk(asset.risk_level) }}</span>
          </div>
          
          <div class="asset-details">
            <div class="detail-row" v-if="asset.profitability">
              <span class="detail-label">Rentabilidade:</span>
              <span class="detail-value">{{ asset.profitability }}% a.a.</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Liquidez:</span>
              <span class="detail-value">D+{{ asset.liquidity_deadline }}</span>
            </div>
            
            <div class="detail-row live-data" v-if="asset.live_data">
              <span class="detail-label">Preço Atual:</span>
              <span class="detail-value highlight">
                {{ formatCurrency(asset.live_data.live_price) }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="glass-card catalog-card" v-else>
        <h3 class="loading-text">Nenhum ativo disponível no momento.</h3>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const assets = ref([]);
const loading = ref(true);

const fetchCatalog = async () => {
  try {
    const res = await api.get('investments/catalog/');
    assets.value = res.data;
  } catch (error) {
    console.error('Erro ao buscar o catálogo:', error);
  } finally {
    loading.value = false;
  }
};

const formatType = (type) => {
  const map = { 'FIXED_INCOME': 'Renda Fixa', 'STOCK': 'Ação', 'FII': 'Fundo Imobiliário' };
  return map[type] || type;
};

const formatRisk = (risk) => {
  const map = { 'LOW': 'Baixo', 'MEDIUM': 'Médio', 'HIGH': 'Alto' };
  return map[risk] || risk;
};

const formatCurrency = (val) => {
  if (!val) return 'R$ 0,00';
  return parseFloat(val).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

onMounted(() => {
  fetchCatalog();
});
</script>

<style scoped>
.catalog-layout { display: flex; flex-direction: column; }
.catalog-content { flex: 1; padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; text-align: left; }
.title { font-size: 2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }
.catalog-card { padding: 40px !important; text-align: center; min-height: 200px; display: flex; align-items: center; justify-content: center; }
.loading-text { color: var(--text-main); font-weight: 400; }

.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.asset-card {
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.asset-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(212, 175, 55, 0.1);
}

.asset-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid var(--border-glass); padding-bottom: 12px; }
.asset-name { font-size: 1.25rem; font-weight: 600; color: var(--text-main); }
.asset-ticker { font-size: 0.9rem; background: rgba(255,255,255,0.1); padding: 4px 8px; border-radius: 6px; font-weight: 500; color: var(--gold-accent); }

.asset-tags { display: flex; gap: 8px; margin-bottom: 20px; }
.tag { font-size: 0.8rem; font-weight: 600; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.5px; }
.type-tag { background: rgba(255, 255, 255, 0.05); color: #fff; border: 1px solid rgba(255, 255, 255, 0.1); }
.risk-tag.low { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.risk-tag.medium { background: rgba(245, 158, 11, 0.15); color: #f59e0b; }
.risk-tag.high { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

.asset-details { display: flex; flex-direction: column; gap: 12px; margin-top: auto; }
.detail-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.95rem; }
.detail-label { color: var(--text-muted); }
.detail-value { color: var(--text-main); font-weight: 500; }
.detail-value.highlight { color: #10b981; font-size: 1.1rem; font-weight: 600; }
.live-data { margin-top: 8px; padding-top: 12px; border-top: 1px dashed var(--border-glass); }
</style>