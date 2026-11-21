import { createServer, type Server } from 'node:http';
import { ConfigService } from '@nestjs/config';
import type { Request } from 'express';
import { exportJWK, generateKeyPair, SignJWT } from 'jose';
import { KeycloakIdentitySource } from './keycloak.identity-source';

describe('Keycloak: assinatura real, issuer, audiência e papéis', () => {
  let server: Server;
  let origin: string;
  let identity: KeycloakIdentitySource;
  let key: Awaited<ReturnType<typeof generateKeyPair>>['privateKey'];
  beforeAll(async () => {
    const pair = await generateKeyPair('RS256');
    key = pair.privateKey;
    const jwk = await exportJWK(pair.publicKey);
    server = createServer((_req, res) => {
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ keys: [{ ...jwk, kid: 'test-key', alg: 'RS256', use: 'sig' }] }));
    });
    await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', resolve));
    const address = server.address();
    if (!address || typeof address === 'string') throw new Error('Porta indisponível');
    origin = `http://127.0.0.1:${address.port}`;
    identity = new KeycloakIdentitySource(
      new ConfigService({
        keycloak: {
          authServerUrl: origin,
          realm: 'Local',
          clientId: 'secgrad-back',
          jwksTimeout: 3000,
        },
      }),
    );
  });
  afterAll(async () => {
    await new Promise<void>((resolve) => server.close(() => resolve()));
  });
  async function token(
    options: {
      roles?: string[];
      aud?: string;
      issuer?: string;
      expired?: boolean;
      otherKey?: boolean;
    } = {},
  ) {
    return new SignJWT({
      realm_access: { roles: options.roles ?? ['sys_secgrad-users'] },
      azp: 'secgrad-front',
    })
      .setProtectedHeader({ alg: 'RS256', kid: 'test-key' })
      .setSubject('test-user')
      .setIssuer(options.issuer ?? `${origin}/realms/Local`)
      .setAudience(options.aud ?? 'secgrad-back')
      .setExpirationTime(options.expired ? 1 : '5m')
      .sign(options.otherKey ? (await generateKeyPair('RS256')).privateKey : key);
  }
  const extract = (jwt?: string) =>
    identity.extract({ headers: { authorization: jwt ? `Bearer ${jwt}` : undefined } } as Request);
  it('não aceita ausência de token', async () => {
    expect(await extract()).toBeNull();
  });
  it('aceita usuário emitido pelo cliente frontend com audiência do backend', async () => {
    expect(await extract(await token())).toMatchObject({ userId: 'test-user', role: 'USER' });
  });
  it.each([
    { expired: true },
    { issuer: 'http://outro/realms/Local' },
    { otherKey: true },
  ])('rejeita token inválido', async (options) => {
    await expect(extract(await token(options))).rejects.toThrow('Token inválido ou expirado');
  });
  it('rejeita audiência de outro serviço', async () => {
    await expect(extract(await token({ aud: 'outro-back' }))).rejects.toThrow('outro cliente');
  });
  it('rejeita papel não reconhecido', async () => {
    await expect(extract(await token({ roles: ['outro-users'] }))).rejects.toThrow(
      'papel reconhecido',
    );
  });
  it('reconhece precedência de administrador', async () => {
    expect(
      await extract(await token({ roles: ['sys_secgrad-users', 'sys_secgrad-admin'] })),
    ).toMatchObject({ role: 'ADMIN' });
  });
});
