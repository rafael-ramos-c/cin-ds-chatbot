// Provisório: precisa de calibração com o corpus e a métrica de busca reais.
export const LIMITE_DISTANCIA_PROVISORIO = 0.8;
export const FALLBACK_DISTANCE_THRESHOLD = Symbol(
  'FALLBACK_DISTANCE_THRESHOLD',
);

export function readFallbackDistanceThreshold(): number {
  const raw = process.env.FALLBACK_DISTANCE_THRESHOLD;
  if (raw === undefined) return LIMITE_DISTANCIA_PROVISORIO;

  const value = raw.trim();
  const threshold = Number(value);
  // Distância não é probabilidade; não impomos um teto arbitrário de 1.
  if (
    !/^(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?$/i.test(value) ||
    !Number.isFinite(threshold) ||
    threshold < 0
  ) {
    throw new Error(
      'FALLBACK_DISTANCE_THRESHOLD deve ser um número decimal finito não negativo.',
    );
  }
  return threshold;
}
