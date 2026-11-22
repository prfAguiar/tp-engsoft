import { test, expect } from '@playwright/test';
import { buildUniqueUser } from './helpers.js';

test.describe('Fluxo 1: Autenticação e Router Guard', () => {
  test('redireciona rotas protegidas para /login, cadastra usuário, faz login e logout', async ({ page }) => {
    const user = buildUniqueUser('flow1');

    // 1. Tentativa de acesso protegido sem autenticação redireciona para /login
    await page.goto('/');
    await expect(page).toHaveURL(/\/login$/);
    await expect(page.locator('.title')).toHaveText('Entrar na sua Carteira');

    await page.goto('/wallet');
    await expect(page).toHaveURL(/\/login$/);

    // 2. Navega para tela de cadastro (/register)
    await page.locator('a.gold-link', { hasText: 'Crie uma conta' }).click();
    await expect(page).toHaveURL(/\/register$/);

    // 3. Valida erro quando confirmação de senha não coincide
    await page.locator('input[placeholder="Seu nome (opcional)"]').fill(user.firstName);
    await page.locator('input[type="email"]').fill(user.email);
    const pwdInputs = page.locator('input[type="password"]');
    await pwdInputs.nth(0).fill(user.password);
    await pwdInputs.nth(1).fill('SenhaDiferente123!');
    await page.locator('button[type="submit"]').click();
    await expect(page.locator('.error-msg')).toHaveText('As senhas não coincidem.');

    // 4. Corrige confirmação de senha, conclui registro e redireciona para /login
    await pwdInputs.nth(1).fill(user.password);
    await page.locator('button[type="submit"]').click();
    await expect(page).toHaveURL(/\/login$/);

    // 5. Realiza login com credenciais válidas e redireciona para o Dashboard (/)
    await page.locator('input[type="email"]').fill(user.email);
    await page.locator('input[type="password"]').fill(user.password);
    await page.locator('button[type="submit"]').click();

    await expect(page).toHaveURL(/\/$/);
    await expect(page.locator('.title')).toHaveText('Seu Portfólio de Investimentos');
    await expect(page.locator('.user-greeting')).toContainText(`Olá, ${user.firstName}`);

    // 6. Confirma persistência do token JWT e bloqueio de rota guest (/login -> /)
    const storedToken = await page.evaluate(() => localStorage.getItem('jwt_token'));
    expect(storedToken).toBeTruthy();

    await page.goto('/login');
    await expect(page).toHaveURL(/\/$/);

    // 7. Realiza logout pela Navbar e confirma limpeza de sessão
    await page.locator('button.nav-logout').click();
    await expect(page).toHaveURL(/\/login$/);
    const clearedToken = await page.evaluate(() => localStorage.getItem('jwt_token'));
    expect(clearedToken).toBeNull();
  });
});
