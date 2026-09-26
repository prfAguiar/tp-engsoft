<template>
  <div class="wallet-layout">
    <main class="wallet-content">
      <div class="header-section">
        <h2 class="title">Gerenciamento da Carteira</h2>
        <p class="subtitle">Administre seus aportes e acompanhe seu patrimônio.</p>
      </div>

      <div class="wallet-grid">
        <div class="glass-card balance-card">
          <h3>Saldo Total</h3>
          <div class="balance-input-group">
            <span class="currency">R$</span>
            <input type="number" v-model="totalAmount" class="premium-input balance-input" step="0.01" min="0"/>
          </div>
          <button @click="updateWallet" class="premium-btn save-btn" :disabled="loading">{{ loading ? 'Salvando...' : 'Salvar Alterações' }}</button>
          <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>
          <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
        </div>

        <div class="glass-card assets-card">
          <div class="assets-header">
            <h3>Meus Ativos</h3>
            <button @click="showAddForm = !showAddForm" class="premium-btn add-btn">{{ showAddForm ? 'Cancelar' : '+ Adicionar Ativo' }}</button>
          </div>
          
          <div v-if="showAddForm" class="add-asset-form">
            <select v-model="newAsset.investment" class="premium-input sm">
              <option value="" disabled>Selecione um ativo...</option>
              <option v-for="inv in catalog" :key="inv.id" :value="inv.id">{{ inv.name }}</option>
            </select>
            <input v-model="newAsset.amount" placeholder="Valor (R$)" type="number" class="premium-input sm" />
            <button @click="addAsset" class="premium-btn sm-btn">Salvar</button>
          </div>

          <div class="table-container">
            <table class="premium-table">
              <thead>
                <tr><th>Ativo</th><th>Tipo</th><th>Montante</th><th>Ações</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in walletItems" :key="item.id">
                  <td>{{ item.investment_name }}</td><td>{{ item.investment_type }}</td>
                  <td>{{ parseFloat(item.amount).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }) }}</td>
                  <td><button @click="removeAsset(item.id)" class="action-btn delete">Remover</button></td>
                </tr>
                <tr v-if="walletItems.length === 0"><td colspan="4" class="empty-state">Nenhum ativo cadastrado.</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const totalAmount = ref(0.00);
const walletItems = ref([]);
const catalog = ref([]);
const showAddForm = ref(false);
const newAsset = ref({ investment: '', amount: '' });
const loading = ref(false);
const successMessage = ref('');
const errorMessage = ref('');

const fetchWallet = async () => {
  try {
    const response = await api.get('wallets/');
    totalAmount.value = response.data.total_amount;
    walletItems.value = response.data.items || [];
  } catch (error) { console.error("Erro:", error); }
};

const fetchCatalog = async () => {
  try {
    const response = await api.get('investments/catalog/');
    catalog.value = response.data;
  } catch (error) { console.error("Erro:", error); }
};

const updateWallet = async () => {
  loading.value = true; successMessage.value = ''; errorMessage.value = '';
  try {
    await api.put('wallets/', { total_amount: totalAmount.value });
    successMessage.value = 'Saldo atualizado!'; setTimeout(() => successMessage.value = '', 3000);
  } catch (error) { errorMessage.value = 'Erro ao atualizar saldo.'; } 
  finally { loading.value = false; }
};

const addAsset = async () => {
  if (!newAsset.value.investment || !newAsset.value.amount) return;
  try {
    await api.post('wallets/items/', newAsset.value);
    showAddForm.value = false; newAsset.value = { investment: '', amount: '' };
    fetchWallet();
  } catch (error) { console.error(error); }
};

const removeAsset = async (id) => {
  try {
    await api.delete('wallets/items/' + id + '/');
    fetchWallet();
  } catch (error) { console.error(error); }
};

onMounted(() => { fetchWallet(); fetchCatalog(); });
</script>

<style scoped>
.wallet-layout { display: flex; flex-direction: column; }
.wallet-content { flex: 1; padding: 40px; max-width: 1200px; margin: 0 auto; width: 100%; }
.header-section { margin-bottom: 40px; }
.title { font-size: 2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }
.wallet-grid { display: grid; grid-template-columns: 1fr; gap: 24px; }
.balance-card, .assets-card { max-width: 100%; }
.balance-card h3 { color: var(--text-muted); font-size: 1.1rem; font-weight: 500; margin-bottom: 16px; }
.balance-input-group { display: flex; align-items: center; background: rgba(0, 0, 0, 0.3); border: 1px solid var(--border-glass); border-radius: 8px; padding: 0 16px; margin-bottom: 20px; max-width: 300px; }
.currency { color: var(--gold-accent); font-weight: 600; font-size: 1.2rem; margin-right: 8px; }
.balance-input { background: transparent; border: none; font-size: 1.5rem; font-weight: 600; padding: 16px 0; margin-top: 0; width: 100%; }
.balance-input:focus { outline: none; }
.success-msg { color: #10b981; margin-top: 12px; font-size: 0.9rem; }
.error-msg { color: #ef4444; margin-top: 12px; font-size: 0.9rem; }
.assets-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.assets-header h3 { color: var(--text-main); font-size: 1.3rem; }
.add-btn { padding: 8px 16px; font-size: 0.9rem; width: auto; }
.add-asset-form { display: flex; gap: 12px; margin-bottom: 24px; padding: 16px; background: rgba(255, 255, 255, 0.02); border-radius: 8px; border: 1px solid var(--border-glass); }
.premium-input.sm { padding: 8px 12px; margin-top: 0; }
.sm-btn { padding: 8px 16px; width: auto; }
.premium-table { width: 100%; border-collapse: collapse; text-align: left; }
.premium-table th { padding: 12px; border-bottom: 1px solid var(--border-glass); color: var(--text-muted); font-weight: 500; }
.premium-table td { padding: 16px 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.02); color: var(--text-main); }
.action-btn.delete { background: transparent; border: 1px solid #ef4444; color: #ef4444; padding: 6px 12px; border-radius: 4px; cursor: pointer; transition: all 0.2s; }
.action-btn.delete:hover { background: #ef4444; color: #fff; }
.empty-state { text-align: center; color: var(--text-muted); padding: 40px !important; }
</style>

