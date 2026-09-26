<template>
  <div class="suggestion-layout">
    <main class="suggestion-content">
      <div class="header-section">
        <h2 class="title">Inteligência de Aportes</h2>
        <p class="subtitle">Descubra exatamente como dividir seu dinheiro hoje, com base no seu perfil e no rebalanceamento inteligente da sua carteira.</p>
      </div>

      <div class="glass-card input-card">
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
      
      <div class="glass-card result-placeholder" v-if="loading">
        <h3 class="loading-text">Analisando o mercado e sua carteira atual...</h3>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const investmentAmount = ref(null);
const loading = ref(false);

const generateSuggestions = () => {
  loading.value = true;
  setTimeout(() => { loading.value = false; }, 2000);
};
</script>

<style scoped>
.suggestion-layout { display: flex; flex-direction: column; }
.suggestion-content { flex: 1; padding: 40px; max-width: 900px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; text-align: center; }
.title { font-size: 2.2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; line-height: 1.5; }
.input-card { padding: 50px !important; text-align: center; margin-bottom: 30px; }
.input-title { font-size: 1.5rem; color: var(--text-main); margin-bottom: 30px; font-weight: 500; }
.input-wrapper { display: flex; flex-direction: column; gap: 20px; max-width: 400px; margin: 0 auto; }
.big-input { font-size: 1.8rem; text-align: center; padding: 20px; background: rgba(0,0,0,0.4); }
.big-btn { font-size: 1.2rem; padding: 18px; }
.result-placeholder { padding: 60px !important; text-align: center; }
.loading-text { color: var(--gold-accent); font-weight: 500; font-size: 1.2rem; }
</style>