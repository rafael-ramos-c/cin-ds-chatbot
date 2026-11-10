import { defineConfig } from 'vitest/config';
import tsconfigPaths from 'vite-tsconfig-paths';

const destino = process.env.BACK_REF03_EVIDENCE_DIR;
if (!destino) throw new Error('BACK_REF03_EVIDENCE_DIR obrigatório');

export default defineConfig({
  plugins: [tsconfigPaths()],
  test: {
    globals: true,
    include: ['src/**/*.spec.ts', 'test/**/*.spec.ts'],
    exclude: ['test/sprint3-v2/**'],
    reporters: ['default', 'json'],
    outputFile: { json: `${destino}/vitest-results.json` },
    coverage: {
      provider: 'v8',
      include: ['src/ai-service/ai-service.service.ts'],
      reporter: ['text', 'json', 'json-summary', 'html'],
      reportsDirectory: `${destino}/coverage`,
      reportOnFailure: true,
    },
  },
});
