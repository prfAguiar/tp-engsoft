import { defineConfig, devices } from '@playwright/test';

process.env.LD_LIBRARY_PATH = `${process.env.HOME}/.cache/ms-playwright/chromium-1161/chrome-linux:${process.env.LD_LIBRARY_PATH || ''}`;

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  fullyParallel: false,
  workers: 1,
  reporter: 'list',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    headless: true,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      command: '../.venv/bin/python manage.py migrate && ../.venv/bin/python manage.py seed_investments && ../.venv/bin/python manage.py runserver 8000 --noreload',
      cwd: '../backend',
      url: 'http://localhost:8000/api/users/profile/quiz/questions/',
      reuseExistingServer: true,
      timeout: 30000,
    },
    {
      command: 'npm run dev -- --port 5173',
      url: 'http://localhost:5173',
      reuseExistingServer: true,
      timeout: 30000,
    },
  ],
});
