import path from 'node:path';
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.spec.ts', 'src/**/*.test.ts', 'test/**/*.spec.ts'],
    exclude: ['node_modules', 'dist', 'test/sprint3-v2/**', 'test/generation-live.e2e-spec.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['src/**/*.ts'],
      exclude: [
        'src/**/*.module.ts',
        'src/**/*.dto.ts',
        'src/**/*.entity.ts',
        'src/main.ts',
        'src/database/**',
        'src/**/*.spec.ts',
        'src/**/*.test.ts',
      ],
    },
    root: '.',
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
});
