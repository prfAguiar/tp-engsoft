import { test, expect } from '@playwright/test';
import { registerAndLoginViaUI } from './helpers.js';

test.describe('Fluxo 4: Minha Carteira e Projeção de Rendimentos no Dashboard', () => {
  test('adiciona ativo na carteira (/wallet), atualiza patrimônio e renderiza projeção no Dashboard (/)', async ({ page }) => {
    await registerAndLoginViaUI(page, 'flow4');

    // 1. Verifica Empty State inicial no Dashboard recém-criado
    const statCards = page.locator('.stats-grid .stat-card');
    await expect(statCards.nth(0).locator('.stat-value')).toContainText('0,00');
    await expect(statCards.nth(1).locator('.stat-value')).toHaveText('N/A');
    await expect(page.locator('.empty-state')).toContainText('Você ainda não possui ativos na carteira.');

    // 2. Navega para Minha Carteira (/wallet) e verifica carteira inicialmente vazia
    await page.locator('nav.premium-navbar a.nav-link', { hasText: 'Minha Carteira' }).click();
    await expect(page).toHaveURL(/\/wallet$/);
    await expect(page.locator('.balance-value')).toContainText('0,00');
    await expect(page.locator('.premium-table .empty-state')).toContainText('Nenhum ativo cadastrado.');

    // 3. Abre formulário "+ Adicionar Ativo", aguarda catálogo e adiciona R$ 5.000 em Tesouro Selic 2029
    await page.locator('button.add-btn').click();
    const assetSelect = page.locator('.add-asset-form select');
    await expect(assetSelect.locator('option', { hasText: 'Tesouro Selic 2029' })).toBeAttached({ timeout: 25000 });
    await assetSelect.selectOption({ label: 'Tesouro Selic 2029' });
    await page.locator('.add-asset-form input[type="number"]').fill('5000');
    await page.locator('button.save-btn', { hasText: 'Salvar' }).click();

    // 4. Confirma atualização imediata da tabela e do Patrimônio Total alocado (R$ 5.000,00)
    const rows = page.locator('.premium-table tbody tr');
    await expect(rows).toHaveCount(1);
    await expect(rows.first()).toContainText('Tesouro Selic 2029');
    await expect(rows.first()).toContainText('5.000,00');
    await expect(page.locator('.balance-value')).toContainText('5.000,00');

    // 5. Retorna ao Dashboard (/) e valida Saldo Total, Rentabilidade Projetada e gráficos Chart.js
    await page.locator('nav.premium-navbar a.nav-link', { hasText: 'Dashboard' }).click();
    await expect(page).toHaveURL(/\/$/);
    await expect(statCards.nth(0).locator('.stat-value')).toContainText('5.000,00');
    await expect(statCards.nth(1).locator('.stat-value')).toContainText('+ 10.5% (Proj. 12m)');
    await expect(page.locator('.charts-grid canvas')).toHaveCount(2);

    // 6. Volta à Carteira (/wallet), remove o ativo e confirma que o saldo retorna a R$ 0,00
    await page.locator('nav.premium-navbar a.nav-link', { hasText: 'Minha Carteira' }).click();
    await page.locator('button.action-btn.delete', { hasText: 'Remover' }).click();
    await expect(page.locator('.balance-value')).toContainText('0,00');
    await expect(page.locator('.premium-table .empty-state')).toContainText('Nenhum ativo cadastrado.');
  });
});
