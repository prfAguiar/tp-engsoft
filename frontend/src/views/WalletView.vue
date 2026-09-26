<template>
  <div class="wallet-layout">
    <main class="wallet-content">
      <div class="header-section">
        <h2 class="title">Gerenciamento da Carteira</h2>
        <p class="subtitle">Administre seus aportes e acompanhe seu patrimônio em tempo real.</p>
      </div>

      <div class="wallet-grid">
        <div class="glass-card balance-card">
          <h3>Patrimônio Total alocado</h3>
          
          <div class="balance-display">
            <span class="balance-value">{{ formatCurrency(totalAmount) }}</span>
          </div>
        </div>

        <div class="glass-card assets-card">
          <div class="assets-header">
            <h3>Meus Ativos</h3>
            <button @click="showAddForm = !showAddForm" :class="['premium-btn', 'add-btn', {'cancel-btn': showAddForm}]">{{ showAddForm ? 'Cancelar' : '+ Adicionar Ativo' }}</button>
          </div>
          
          <div v-if="showAddForm" class="add-asset-form">
            <select v-model="newAsset.investment" class="premium-input sm">
              <option value="" disabled>Selecione um ativo...</option>
              <option v-for="inv in catalog" :key="inv.id" :value="inv.id">{{ inv.name }}</option>
            </select>
            <input v-model="newAsset.amount" placeholder="Valor (R$)" type="number" class="premium-input sm" />
            <button @click="addAsset" class="premium-btn sm-btn save-btn">Salvar</button>
          </div>

          <div class="table-container">
            <table class="premium-table">
              <thead>
                <tr><th>Ativo</th><th>Tipo</th><th>Montante</th><th>Ações</th></tr>
              </thead>
              <tbody>
                <tr v-for="item in walletItems" :key="item.id">
                  <td>{{ item.investment_name }}</td>
                  <td><span class="type-tag">{{ item.investment_type }}</span></td>
                  <td class="money-cell">{{ formatCurrency(item.amount) }}</td>
                  <td><button @click="removeAsset(item.id)" class="action-btn delete">Remover</button></td>
                </tr>
                <tr v-if="walletItems.length === 0"><td colspan="4" class="empty-state">Nenhum ativo cadastrado. Adicione um ativo para compor sua carteira.</td></tr>
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

const formatCurrency = (val) => {
  return parseFloat(val || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

const fetchWallet = async () => {
  try {
    const response = await api.get('wallets/');
    walletItems.value = response.data.items || [];
    let calculatedTotal = 0;
    walletItems.value.forEach(item => {
      calculatedTotal += parseFloat(item.amount) || 0;
    });
    totalAmount.value = calculatedTotal;
  } catch (error) { console.error("Erro:", error); }
};

const fetchCatalog = async () => {
  try {
    const response = await api.get('investments/catalog/');
    catalog.value = response.data;
  } catch (error) { console.error("Erro:", error); }
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
.title { font-size: 2.2rem; font-weight: 600; margin-bottom: 8px; color: var(--gold-accent); }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }

/* REFACTORED GRID */
.wallet-grid { 
  display: grid; 
  grid-template-columns: 350px 1fr; 
  gap: 24px; 
  align-items: start;
}
@media (max-width: 900px) {
  .wallet-grid { grid-template-columns: 1fr; }
}

/* BALANCE CARD */
.balance-card { text-align: center; padding: 30px !important; }
.balance-card h3 { color: var(--text-muted); font-size: 1.1rem; font-weight: 500; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }

.balance-display { display: flex; flex-direction: column; align-items: center; gap: 15px; }
.balance-value { font-size: 2.5rem; font-weight: 700; color: #fff; }


/* ASSETS CARD */
.assets-card { padding: 30px !important; }
.assets-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid var(--border-glass); }
.assets-header h3 { color: var(--text-main); font-size: 1.4rem; font-weight: 600; }
.add-btn { padding: 8px 16px; font-size: 0.9rem; width: auto; }

.add-asset-form { display: flex; gap: 12px; margin-bottom: 24px; padding: 20px; background: rgba(0, 0, 0, 0.2); border-radius: 12px; border: 1px solid var(--border-glass); }
.premium-input.sm { padding: 10px 14px; margin-top: 0; flex: 1; }
.sm-btn { padding: 10px 20px; width: auto; }

.table-container { overflow-x: auto; }
.premium-table { width: 100%; border-collapse: collapse; text-align: left; }
.premium-table th { padding: 16px; border-bottom: 1px solid var(--border-glass); color: var(--text-muted); font-weight: 500; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 0.5px; }
.premium-table td { padding: 18px 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.02); color: var(--text-main); font-weight: 500; }
.money-cell { color: #fff !important; font-weight: 600 !important; }
.type-tag { background: rgba(255, 255, 255, 0.05); padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; color: var(--text-muted); }

.action-btn.delete { background: transparent; border: 1px solid rgba(239, 68, 68, 0.3); color: #ef4444; padding: 6px 14px; border-radius: 6px; cursor: pointer; transition: all 0.2s; font-size: 0.85rem; font-weight: 500; }
.action-btn.delete:hover { background: rgba(239, 68, 68, 0.15); border-color: #ef4444; }

.empty-state { text-align: center; color: var(--text-muted); padding: 60px !important; font-style: italic; }
.cancel-btn { background: #ef4444 !important; color: #fff !important; border: none !important; }
.cancel-btn:hover { background: #dc2626 !important; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3) !important; }

.save-btn { background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important; color: #fff !important; border: none !important; }
.save-btn:hover { box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3) !important; transform: translateY(-2px); }
</style>