/** Opt-in: integração com FastAPI/Chroma reais e JWT/JWKS locais.
 * Apenas PostgreSQL é substituído. Não comprova o servidor Keycloak/LDAP.
 */
import 'reflect-metadata';
import { createServer, type Server } from 'node:http';
import { type INestApplication } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Test } from '@nestjs/testing';
import { exportJWK, generateKeyPair, SignJWT } from 'jose';
import request from 'supertest';
import { AppModule } from '../src/app.module';
import { configureApp } from '../src/configure-app';
import { PrismaService } from '../src/database/prisma.service';

describe.skipIf(process.env.SECGRAD_LIVE_TEST !== '1')(
  'JWT + NestJS + FastAPI/Chroma reais (banco relacional substituído)',
  () => {
    let app: INestApplication;
    let jwks: Server;
    let jwt: string;
    beforeAll(async () => {
      const pair = await generateKeyPair('RS256');
      const key = await exportJWK(pair.publicKey);
      jwks = createServer((_req, res) => {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ keys: [{ ...key, alg: 'RS256', use: 'sig', kid: 'live-test' }] }));
      });
      await new Promise<void>((resolve) => jwks.listen(0, '127.0.0.1', resolve));
      const address = jwks.address();
      if (!address || typeof address === 'string') throw new Error('JWKS indisponível');
      const origin = `http://127.0.0.1:${address.port}`;
      const module = await Test.createTestingModule({ imports: [AppModule] })
        .overrideProvider(PrismaService)
        .useValue({ $connect: async () => {}, $disconnect: async () => {} })
        .compile();
      const config = module.get(ConfigService);
      config.set('keycloak.authServerUrl', origin);
      config.set('keycloak.realm', 'Local');
      config.set('keycloak.jwksUrl', `${origin}/certs`);
      app = module.createNestApplication({ logger: false });
      configureApp(app);
      await app.init();
      jwt = await new SignJWT({
        realm_access: { roles: ['sys_secgrad-users'] },
        azp: 'secgrad-front',
      })
        .setProtectedHeader({ alg: 'RS256', kid: 'live-test' })
        .setSubject('test-user')
        .setIssuer(`${origin}/realms/Local`)
        .setAudience('secgrad-back')
        .setExpirationTime('5m')
        .sign(pair.privateKey);
    });
    afterAll(async () => {
      await app?.close();
      if (jwks) await new Promise<void>((resolve) => jwks.close(() => resolve()));
    });
    it('consulta normas reais com filtro de curso/perfil e trechos associados', async () => {
      const response = await request(app.getHttpServer())
        .post('/secgrad/api/v1/conversa')
        .set('Authorization', `Bearer ${jwt}`)
        .send({
          consulta: {
            pergunta: 'Quais são as condições para realizar estágio?',
            curso: 'CC',
            perfil: 'novo',
            top_k: 3,
          },
        })
        .expect(201);
      const result = response.body.data;
      expect(result.fontes.length).toBeGreaterThan(0);
      expect(
        result.fontes.every(
          (f: { trecho: string }) => typeof f.trecho === 'string' && f.trecho.length > 0,
        ),
      ).toBe(true);
      expect(result.contexto).toContain('Documento:');
      expect(typeof result.distancia_minima).toBe('number');
    }, 60000);
  },
);
