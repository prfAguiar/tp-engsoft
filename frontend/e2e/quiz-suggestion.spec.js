import { test, expect } from '@playwright/test';
import { registerAndLoginViaUI } from './helpers.js';

test.describe('Fluxo 2: Quiz de Perfil de Investidor e Sugestão de Alocação', () => {
  test('responde as 4 perguntas do Quiz (/quiz), classifica perfil Moderado e gera sugestão de alocação (/suggestion)', async ({ page }) => {
    await registerAndLoginViaUI(page, 'flow2');

    // 1. Navega pela Navbar para Descobrir Perfil (/quiz)
    await page.locator('nav.premium-navbar a.nav-link', { hasText: 'Descobrir Perfil' }).click();
    await expect(page).toHaveURL(/\/quiz$/);
    await expect(page.locator('.title')).toHaveText('Descubra seu Perfil de Investidor');

    // 2. Responde as 4 perguntas escolhendo a opção intermediária (score 2 -> total 8 = Moderado)
    for (let step = 1; step <= 4; step++) {
      await expect(page.locator('.progress-indicator')).toHaveText(`Pergunta ${step} de 4`);
      const options = page.locator('.options-container .option-btn');
      await expect(options).toHaveCount(3);
      await options.nth(1).click();
      await expect(options.nth(1)).toHaveClass(/selected/);

      if (step < 4) {
        await page.locator('button', { hasText: 'Próxima' }).click();
      } else {
        await page.locator('button', { hasText: 'Concluir' }).click();
      }
    }

    // 3. Verifica o resultado do Quiz (Perfil Moderado, 8 / 12 pontos)
    await expect(page.locator('.result-card .success-text')).toHaveText('Perfil Moderado');
    await expect(page.locator('.result-card .score-text')).toContainText('Pontuação: 8 / 12');

    // 4. Navega para a aba Sugestões (/suggestion) e informa montante de R$ 10.000
    await page.locator('nav.premium-navbar a.nav-link', { hasText: 'Sugestões' }).click();
    await expect(page).toHaveURL(/\/suggestion$/);
    await expect(page.locator('.title')).toHaveText('Inteligência de Aportes');

    const generateBtn = page.locator('button', { hasText: 'Gerar Sugestões' });
    await expect(generateBtn).toBeDisabled();

    await page.locator('input.big-input[type="number"]').fill('10000');
    await expect(generateBtn).toBeEnabled();
    await generateBtn.click();

    // 5. Valida a estratégia Moderada (45% Renda Fixa = R$ 4.500, 30% FII = R$ 3.000, 25% Ações = R$ 2.500)
    await expect(page.locator('.result-header h3')).toHaveText('Estratégia Moderado');
    const cards = page.locator('.allocations-grid .allocation-card');
    await expect(cards).toHaveCount(3);

    const rfCard = cards.filter({ hasText: 'Renda Fixa' });
    await expect(rfCard.locator('.alloc-pct')).toHaveText('45%');
    await expect(rfCard.locator('.alloc-amount')).toContainText('4.500,00');

    const fiiCard = cards.filter({ hasText: 'Fundos Imobiliários' });
    await expect(fiiCard.locator('.alloc-pct')).toHaveText('30%');
    await expect(fiiCard.locator('.alloc-amount')).toContainText('3.000,00');

    const stockCard = cards.filter({ hasText: 'Ações Nacionais' });
    await expect(stockCard.locator('.alloc-pct')).toHaveText('25%');
    await expect(stockCard.locator('.alloc-amount')).toContainText('2.500,00');

    // 6. Testa o botão "Nova Simulação" retornando ao formulário de entrada
    await page.locator('button', { hasText: 'Nova Simulação' }).click();
    await expect(page.locator('.input-title')).toHaveText('Qual montante você deseja investir?');
  });
});
