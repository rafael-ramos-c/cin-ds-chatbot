/**
 * Valida variáveis de ambiente no boot. Falha cedo (na inicialização) em vez de
 * deixar erros de configuração aparecerem só na primeira requisição em produção.
 *
 * Sem dependência extra (Joi/zod): checagens explícitas sobre o objeto de env.
 */
export function validateEnv(config: Record<string, unknown>): Record<string, unknown> {
  const errors: string[] = [];

  for (const key of ['KEYCLOAK_AUTH_SERVER_URL', 'KEYCLOAK_REALM', 'KEYCLOAK_CLIENT_ID']) {
    if (typeof config[key] !== 'string' || !(config[key] as string).trim())
      errors.push(`${key} é obrigatório.`);
  }
  for (const key of ['KEYCLOAK_AUTH_SERVER_URL', 'KEYCLOAK_JWKS_URL', 'AI_SERVICE_URL']) {
    if (!config[key]) continue;
    try {
      const url = new URL(String(config[key]));
      if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password)
        throw new Error();
    } catch {
      errors.push(`${key} deve ser uma URL HTTP(S) sem credenciais.`);
    }
  }

  for (const key of ['KEYCLOAK_JWKS_CACHE_MAX_AGE', 'KEYCLOAK_JWKS_TIMEOUT']) {
    const raw = config[key];
    if (
      raw !== undefined &&
      (!/^\d+$/.test(String(raw)) || Number(raw) < 1 || Number(raw) > 2147483647)
    ) {
      errors.push(`${key} deve ser um número inteiro (ms).`);
    }
  }

  if (errors.length > 0) {
    throw new Error(`Configuração de ambiente inválida:\n- ${errors.join('\n- ')}`);
  }

  return config;
}
