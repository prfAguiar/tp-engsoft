<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="glass-card modal-container">
      <div class="modal-header">
        <div>
          <div class="badge-row">
            <span class="ticker-badge" v-if="asset.ticker">{{ asset.ticker }}</span>
            <span class="type-badge">{{ formatType(asset.type) }}</span>
          </div>
          <h2 class="asset-title">{{ asset.name }}</h2>
          <p class="company-name" v-if="asset.live_data?.long_name">{{ asset.live_data.long_name }}</p>
        </div>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div class="metrics-grid">
        <div class="metric-card" v-if="asset.live_data?.live_price">
          <span class="metric-label">Cotação</span>
          <span class="metric-val highlight">{{ formatCurrency(asset.live_data.live_price) }}</span>
        </div>
        <div class="metric-card" v-else-if="asset.profitability">
          <span class="metric-label">Rentabilidade</span>
          <span class="metric-val highlight">{{ asset.profitability }}% a.a.</span>
        </div>
        <div class="metric-card" v-if="asset.live_data?.dividend_yield_percent">
          <span class="metric-label">Div. Yield</span>
          <span class="metric-val gold">{{ asset.live_data.dividend_yield_percent }}%</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Liquidez</span>
          <span class="metric-val">D+{{ asset.liquidity_deadline }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Risco</span>
          <span :class="['risk-pill', asset.risk_level.toLowerCase()]">{{ formatRisk(asset.risk_level) }}</span>
        </div>
      </div>

      <div class="description-section">
        <h4 class="section-title">Tese do Investimento</h4>
        <p class="description-text">{{ asset.description || 'Ativo selecionado pela corretora com sólida governança e potencial de retorno.' }}</p>
        <p class="sector-info" v-if="asset.live_data?.sector">
          <strong>Setor:</strong> {{ asset.live_data.sector }}
        </p>
      </div>

      <div class="modal-footer">
        <button class="premium-btn close-action" @click="$emit('close')">Concluir Leitura</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ asset: { type: Object, required: true } });
defineEmits(['close']);
const formatType = (type) => ({ 'FIXED_INCOME': 'Renda Fixa', 'STOCK': 'Ação', 'FII': 'Fundo Imobiliário' }[type] || type);
const formatRisk = (risk) => ({ 'LOW': 'Baixo', 'MEDIUM': 'Médio', 'HIGH': 'Alto' }[risk] || risk);
const formatCurrency = (val) => val ? parseFloat(val).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) : 'R$ 0,00';
</script>

<style scoped>
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0, 0, 0, 0.82);
  backdrop-filter: blur(12px); display: flex; align-items: center; justify-content: center;
  z-index: 1000; padding: 20px; animation: fadeIn 0.25s ease-out;
}
.modal-container {
  max-width: 580px; width: 100%; border: 1px solid rgba(212, 175, 55, 0.4);
  background: rgba(14, 16, 24, 0.96); box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px var(--gold-glow);
  padding: 30px !important; animation: scaleUp 0.25s ease-out;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
.modal-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; border-bottom: 1px solid var(--border-glass); padding-bottom: 14px; }
.badge-row { display: flex; gap: 8px; margin-bottom: 6px; }
.ticker-badge { background: rgba(212, 175, 55, 0.15); color: var(--gold-accent); padding: 3px 10px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(212, 175, 55, 0.3); }
.type-badge { background: rgba(255, 255, 255, 0.05); color: var(--text-muted); padding: 3px 10px; border-radius: 6px; font-size: 0.85rem; }
.asset-title { font-size: 1.55rem; color: #fff; font-weight: 600; }
.company-name { font-size: 0.88rem; color: var(--text-muted); margin-top: 2px; }
.close-btn { background: none; border: none; color: var(--text-muted); font-size: 1.8rem; cursor: pointer; transition: color 0.2s; line-height: 1; }
.close-btn:hover { color: var(--gold-accent); }
.metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 10px; margin-bottom: 20px; }
.metric-card { background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-glass); padding: 10px; border-radius: 10px; text-align: center; }
.metric-label { font-size: 0.72rem; color: var(--text-muted); display: block; margin-bottom: 4px; text-transform: uppercase; }
.metric-val { font-size: 1.05rem; font-weight: 600; color: #fff; }
.metric-val.highlight { color: #10b981; }
.metric-val.gold { color: var(--gold-accent); }
.risk-pill { font-size: 0.8rem; font-weight: 600; padding: 2px 8px; border-radius: 12px; display: inline-block; }
.risk-pill.low { color: #10b981; background: rgba(16, 185, 129, 0.15); }
.risk-pill.medium { color: #f59e0b; background: rgba(245, 158, 11, 0.15); }
.risk-pill.high { color: #ef4444; background: rgba(239, 68, 68, 0.15); }
.description-section { background: rgba(0, 0, 0, 0.35); border: 1px solid var(--border-glass); border-radius: 10px; padding: 14px; margin-bottom: 20px; }
.section-title { font-size: 0.82rem; color: var(--gold-accent); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
.description-text { font-size: 0.92rem; color: var(--text-main); line-height: 1.45; }
.sector-info { font-size: 0.82rem; color: var(--text-muted); margin-top: 8px; }
.modal-footer { display: flex; justify-content: flex-end; }
.close-action { width: auto; padding: 10px 24px; }
</style>
