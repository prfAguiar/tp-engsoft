<template>
  <div class="suggestion-layout">
    <main class="suggestion-content">
      <div class="header-section">
        <h2 class="title">Inteligência de Aportes</h2>
        <p class="subtitle">Descubra exatamente como dividir seu dinheiro hoje, com base no seu perfil e no rebalanceamento inteligente da sua carteira.</p>
      </div>

      <div class="glass-card input-card" v-if="!resultData && !loading">
        <h3 class="input-title">Qual montante você deseja investir?</h3>
        <div class="input-wrapper">
          <input 
            type="number" 
            v-model="investmentAmount" 
            placeholder="Ex: 5000" 
            class="premium-input big-input"
            min="1"
          />
          <button @click="generateSuggestions" class="premium-btn big-btn" :disabled="!investmentAmount || investmentAmount <= 0">Gerar Sugestões</button>
        </div>
      </div>
      
      <div class="glass-card result-placeholder" v-else-if="loading">
        <h3 class="loading-text">Analisando o mercado e sua carteira atual...</h3>
      </div>
      
      <div v-if="resultData" class="suggestion-results fade-in">
        <div class="result-header">
          <h3>Estratégia {{ resultData.profile_label }}</h3>
          <p v-if="resultData.rebalanced" class="rebalance-notice">Sua carteira atual de <strong>{{ formatCurrency(resultData.current_portfolio_total) }}</strong> foi considerada no cálculo para rebalanceamento automático.</p>
        </div>
        
        <div class="allocations-grid">
          <div class="glass-card allocation-card" v-for="alloc in resultData.allocations" :key="alloc.type">
            <div class="alloc-header">
              <span class="alloc-category">{{ alloc.category }}</span>
              <span class="alloc-pct highlight">{{ alloc.allocation_percentage }}%</span>
            </div>
            
            <div class="alloc-amount">
              {{ formatCurrency(alloc.allocated_amount) }}
            </div>
            
            <div class="alloc-description">
              <p class="meta-text">Meta ideal do seu perfil: {{ alloc.target_percentage }}%</p>
              <p class="desc-text">{{ alloc.description }}</p>
            </div>
            
            <div class="suggested-assets">
              <h4>Ativos Recomendados:</h4>
              <div class="tags-container">
                <span class="asset-tag" v-for="asset in alloc.suggested_assets" :key="asset">{{ asset }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="reset-action">
          <button @click="resultData = null; investmentAmount = null" class="premium-btn outline">Nova Simulação</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const investmentAmount = ref(null);
const loading = ref(false);
const resultData = ref(null);

const generateSuggestions = async () => {
  loading.value = true;
  resultData.value = null;
  try {
    const res = await api.post('investments/suggest/', { amount: investmentAmount.value });
    resultData.value = res.data;
  } catch (error) {
    console.error('Erro ao buscar sugestões:', error);
    alert('Você precisa realizar o Teste de Perfil primeiro!');
  } finally {
    loading.value = false;
  }
};

const formatCurrency = (val) => {
  if (val === null || val === undefined) return 'R$ 0,00';
  return parseFloat(val).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};
</script>

<style scoped>
.suggestion-layout { display: flex; flex-direction: column; }
.suggestion-content { flex: 1; padding: 40px; max-width: 1000px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; text-align: center; }
.title { font-size: 2.2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; line-height: 1.5; }

.input-card { padding: 50px !important; text-align: center; margin-bottom: 30px; }
.input-title { font-size: 1.5rem; color: var(--text-main); margin-bottom: 30px; font-weight: 500; }
.input-wrapper { display: flex; flex-direction: column; gap: 20px; max-width: 400px; margin: 0 auto; }
.big-input { font-size: 1.8rem; text-align: center; padding: 20px; background: rgba(0,0,0,0.4); border: 2px solid rgba(212, 175, 55, 0.2); }
.big-input:focus { border-color: var(--gold-accent); }
.big-btn { font-size: 1.2rem; padding: 18px; }

.result-placeholder { padding: 60px !important; text-align: center; margin-bottom: 30px; }
.loading-text { color: var(--gold-accent); font-weight: 500; font-size: 1.2rem; }

.fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.result-header { text-align: center; margin-bottom: 40px; }
.result-header h3 { font-size: 2rem; color: var(--gold-accent); margin-bottom: 12px; }
.rebalance-notice { color: #10b981; font-size: 1rem; padding: 10px; background: rgba(16, 185, 129, 0.1); border-radius: 8px; display: inline-block; }

.allocations-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 40px; }
.allocation-card { padding: 24px !important; display: flex; flex-direction: column; }
.alloc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid var(--border-glass); padding-bottom: 12px; }
.alloc-category { font-size: 1.2rem; font-weight: 600; color: var(--text-main); }
.alloc-pct { font-size: 1.2rem; font-weight: 700; color: var(--gold-accent); }
.alloc-amount { font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 20px; }

.alloc-description { flex: 1; margin-bottom: 20px; }
.meta-text { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 8px; }
.desc-text { font-size: 0.95rem; color: var(--text-main); line-height: 1.4; opacity: 0.9; }

.suggested-assets h4 { font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
.tags-container { display: flex; flex-wrap: wrap; gap: 8px; }
.asset-tag { background: rgba(212, 175, 55, 0.15); color: var(--gold-accent); padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; border: 1px solid rgba(212, 175, 55, 0.3); }

.reset-action { display: flex; justify-content: center; }
</style>