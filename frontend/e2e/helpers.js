import { expect } from '@playwright/test';

export const DEFAULT_E2E_PASSWORD = 'K9#mP2!xQ7vL';

export function buildUniqueUser(prefix = 'e2e') {
  const uniqueId = `${Date.now()}_${Math.floor(Math.random() * 100000)}`;
  return {
    firstName: 'Investidor',
    email: `${prefix}.${uniqueId}@finless.com`,
    password: DEFAULT_E2E_PASSWORD,
  };
}

export async function registerAndLoginViaUI(page, prefix = 'e2e') {
  const user = buildUniqueUser(prefix);

  await page.goto('/register');
  await page.locator('input[placeholder="Seu nome (opcional)"]').fill(user.firstName);
  await page.locator('input[type="email"]').fill(user.email);
  const passwordInputs = page.locator('input[type="password"]');
  await passwordInputs.nth(0).fill(user.password);
  await passwordInputs.nth(1).fill(user.password);
  await page.locator('button[type="submit"]').click();

  await expect(page).toHaveURL(/\/login$/);

  await page.locator('input[type="email"]').fill(user.email);
  await page.locator('input[type="password"]').fill(user.password);
  await page.locator('button[type="submit"]').click();

  await expect(page).toHaveURL(/\/$/);
  await expect(page.locator('.user-greeting')).toContainText(user.firstName);

  return user;
}
