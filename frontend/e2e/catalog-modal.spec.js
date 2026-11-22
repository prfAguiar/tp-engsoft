import { test, expect } from '@playwright/test';
import { registerAndLoginViaUI } from './helpers.js';

test.describe('Fluxo 3: Catálogo de Ativos e Modal de Detalhes Premium', () => {
  test('navega até Mercado (/catalog), lista ativos e exibe o InvestmentDetailModal com tese e métricas', async ({ page }) => {
    await registerAndLoginViaUI(page, 'flow3');

    // 1. Navega pela Navbar para a aba Mercado (/catalog)
    await page.locator('nav.premium-navbar a.nav-link', { hasText: 'Mercado' }).click();
    await expect(page).toHaveURL(/\/catalog$/);
    await expect(page.locator('.title')).toHaveText('Mercado Financeiro');

    // 2. Aguarda carregamento dos cards de ativos (seeded no banco)
    const assetCards = page.locator('.catalog-grid .asset-card');
    await expect(assetCards.first()).toBeVisible({ timeout: 20000 });
    expect(await assetCards.count()).toBeGreaterThanOrEqual(3);

    // 3. Localiza card de Renda Fixa (Tesouro Selic 2029) e valida tags e informações
    const selicCard = assetCards.filter({ hasText: 'Tesouro Selic 2029' });
    await expect(selicCard).toBeVisible();
    await expect(selicCard.locator('.type-tag')).toHaveText('Renda Fixa');
    await expect(selicCard.locator('.risk-tag')).toContainText('Risco Baixo');

    // 4. Clica no card para abrir o InvestmentDetailModal.vue
    await selicCard.click();
    const modal = page.locator('.modal-container');
    await expect(modal).toBeVisible();
    await expect(modal.locator('.asset-title')).toHaveText('Tesouro Selic 2029');
    await expect(modal.locator('.type-badge')).toHaveText('Renda Fixa');
    await expect(modal.locator('.section-title')).toHaveText('Tese do Investimento');
    await expect(modal.locator('.description-text')).not.toBeEmpty();
    await expect(modal.locator('.metrics-grid')).toContainText('Liquidez');
    await expect(modal.locator('.metrics-grid')).toContainText('Risco');

    // 5. Fecha o modal pelo botão Concluir Leitura
    await modal.locator('button.close-action', { hasText: 'Concluir Leitura' }).click();
    await expect(modal).toBeHidden();

    // 6. Abre outro card com ticker B3 (Itaú Unibanco) e fecha pelo botão "×"
    const stockCard = assetCards.filter({ hasText: 'Itaú Unibanco' });
    await stockCard.click();
    await expect(modal).toBeVisible();
    await expect(modal.locator('.ticker-badge')).toHaveText('ITUB4.SA');
    await expect(modal.locator('.type-badge')).toHaveText('Ação');
    await modal.locator('button.close-btn').click();
    await expect(modal).toBeHidden();
  });
});
