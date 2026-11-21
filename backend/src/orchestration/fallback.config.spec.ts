import { readFallbackDistanceThreshold } from './fallback.config';

describe('fallback config', () => {
  afterEach(() => vi.unstubAllEnvs());

  it('usa 0.8 provisório somente quando a variável está ausente', () => {
    vi.stubEnv('FALLBACK_DISTANCE_THRESHOLD', undefined);
    expect(readFallbackDistanceThreshold()).toBe(0.8);
  });

  it.each([
    '',
    ' ',
    '-0.1',
    'NaN',
    'Infinity',
    '1e999',
    'abc',
    '0.8abc',
    '0,8',
    '0x10',
  ])('rejeita configuração inválida %j', (raw) => {
    vi.stubEnv('FALLBACK_DISTANCE_THRESHOLD', raw);
    expect(() => readFallbackDistanceThreshold()).toThrow(
      'FALLBACK_DISTANCE_THRESHOLD deve ser um número decimal finito não negativo.',
    );
  });

  it.each([
    ['0', 0],
    ['0.5', 0.5],
    [' 0.9 ', 0.9],
    ['1.2', 1.2],
    ['8e-1', 0.8],
  ])('aceita %s sem impor teto de probabilidade', (raw, expected) => {
    vi.stubEnv('FALLBACK_DISTANCE_THRESHOLD', raw);
    expect(readFallbackDistanceThreshold()).toBe(expected);
  });
});
