<template>
  <div class="wallet-layout">
    <main class="wallet-content">
      <div class="header-section">
        <h2 class="title">Gerenciamento da Carteira</h2>
        <p class="subtitle">Administre seus aportes e acompanhe seu patrimônio.</p>
      </div>

      <div class="wallet-grid">
        <!-- Card de Patrimônio Total -->
        <div class="glass-card balance-card">
          <h3>Saldo Total</h3>
          <div class="balance-input-group">
            <span class="currency">R$</span>
            <input 
              type="number" 
              v-model="totalAmount" 
              class="premium-input balance-input"
              step="0.01"
              min="0"
            />
          </div>
          <button @click="updateWallet" class="premium-btn save-btn" :disabled="loading">
            {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
          <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>
          <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const totalAmount = ref(0.00);
const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const fetchWallet = async () => {
  try {
    const response = await api.get('wallets/');
    totalAmount.value = response.data.total_amount;
  } catch (error) {
    console.error("Erro ao carregar carteira:", error);
  }
};

const updateWallet = async () => {
  loading.value = true;
  successMessage.value = '';
  errorMessage.value = '';
  
  try {
    await api.put('wallets/', { total_amount: totalAmount.value });
    successMessage.value = 'Saldo atualizado com sucesso!';
    setTimeout(() => successMessage.value = '', 3000);
  } catch (error) {
    errorMessage.value = 'Erro ao atualizar saldo.';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchWallet();
});
</script>

<style scoped>
.wallet-layout {
  display: flex;
  flex-direction: column;
}

.wallet-content {
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

.wallet-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.balance-card {
  max-width: 500px;
}

.balance-card h3 {
  color: var(--text-muted);
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 16px;
}

.balance-input-group {
  display: flex;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--border-glass);
  border-radius: 8px;
  padding: 0 16px;
  margin-bottom: 20px;
}

.currency {
  color: var(--gold-accent);
  font-weight: 600;
  font-size: 1.2rem;
  margin-right: 8px;
}

.balance-input {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  font-weight: 600;
  padding: 16px 0;
  margin-top: 0;
  width: 100%;
}

.balance-input:focus {
  outline: none;
  border-color: transparent;
}

.save-btn {
  margin-top: 8px;
}

.success-msg {
  color: #10b981;
  margin-top: 12px;
  font-size: 0.9rem;
}

.error-msg {
  color: #ef4444;
  margin-top: 12px;
  font-size: 0.9rem;
}
</style>
