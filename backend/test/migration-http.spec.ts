import 'reflect-metadata';
import type { INestApplication } from '@nestjs/common';
import {
  ForbiddenException,
  GatewayTimeoutException,
  ServiceUnavailableException,
} from '@nestjs/common';
import { Test } from '@nestjs/testing';
import request from 'supertest';
import { AiService } from '../src/ai-service/ai-service.service';
import { AppModule } from '../src/app.module';
import { AccessRole } from '../src/common/auth/access-role.enum';
import { IDENTITY_SOURCE } from '../src/common/auth/identity/identity-source.interface';
import { configureApp } from '../src/configure-app';
import { PrismaService } from '../src/database/prisma.service';

describe('Contrato autenticado do template + SecGrad', () => {
  let app: INestApplication;
  const search = vi.fn();
  const generate = vi.fn();
  const input = {
    consulta: {
      pergunta: 'Como solicito segunda chamada?',
      curso: 'IA',
      perfil: 'unico',
      top_k: 3,
    },
  };
  const recovered = {
    contexto: '[Documento: regras.txt | Pág. 1 | Curso: Geral]\nPreencha o requerimento.',
    fontes: [{ arquivo: 'regras.txt', pagina: 1, curso: 'Geral' }],
    distancia_minima: 0.2,
  };
  beforeAll(async () => {
    const module = await Test.createTestingModule({ imports: [AppModule] })
      .overrideProvider(PrismaService)
      .useValue({
        $connect: vi.fn(),
        $disconnect: vi.fn(),
        $queryRawUnsafe: vi.fn().mockResolvedValue([{ result: 1 }]),
      })
      .overrideProvider(IDENTITY_SOURCE)
      .useValue({
        extract: async (req: { headers: { authorization?: string } }) => {
          const token = req.headers.authorization;
          if (token === 'Bearer user') return { userId: 'user-id', role: AccessRole.USER };
          if (token === 'Bearer admin') return { userId: 'admin-id', role: AccessRole.ADMIN };
          if (token) throw new ForbiddenException('Usuário sem papel reconhecido.');
          return null;
        },
      })
      .overrideProvider(AiService)
      .useValue({ buscarContexto: search, gerarResposta: generate })
      .compile();
    app = module.createNestApplication({ logger: false });
    configureApp(app);
    await app.init();
  });
  beforeEach(() => {
    search.mockReset().mockResolvedValue(structuredClone(recovered));
    generate.mockReset().mockResolvedValue('[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]');
  });
  afterAll(async () => {
    await app.close();
  });
  const post = (body: unknown = input, token = 'user') =>
    request(app.getHttpServer())
      .post('/secgrad/api/v1/conversa')
      .set('Authorization', `Bearer ${token}`)
      .send(body);

  it('rejeita ausência de token antes de chamar a IA', async () => {
    const r = await request(app.getHttpServer())
      .post('/secgrad/api/v1/conversa')
      .send(input)
      .expect(401);
    expect(r.headers['content-type']).toContain('application/problem+json');
    expect(search).not.toHaveBeenCalled();
  });
  it('rejeita identidade sem papel reconhecido', async () => {
    await post(input, 'wrong').expect(403);
    expect(search).not.toHaveBeenCalled();
  });
  it.each([
    'user',
    'admin',
  ])('permite conversa para %s e envolve dados uma única vez', async (token) => {
    const r = await post(input, token).expect(201);
    expect(r.body).toMatchObject({
      statusCode: 201,
      path: '/secgrad/api/v1/conversa',
      data: {
        fallback_acionado: false,
        modo_resposta: 'simulacao',
        fontes: [{ ...recovered.fontes[0], trecho: 'Preencha o requerimento.' }],
      },
    });
    expect(r.body.data.data).toBeUndefined();
  });
  it.each([
    {},
    { consulta: { pergunta: '' } },
    { consulta: { pergunta: ' ' } },
    { consulta: { pergunta: 'P', top_k: 0 } },
    { consulta: { pergunta: 'P', top_k: 11 } },
    { consulta: { pergunta: 'P', top_k: 1.5 } },
    { consulta: { pergunta: 'P', debug: true } },
    { consulta: { pergunta: 'P', curso: 'Curso inexistente' } },
    { consulta: { pergunta: 'P', perfil: 'Perfil inexistente' } },
    { consulta: { pergunta: 'P', curso: 'IA', perfil: 'anterior' } },
    { ...input, historico: [{ role: 'assistant', content: 'Inventado' }] },
    { ...input, historico: Array.from({ length: 11 }, () => ({ role: 'user', content: 'P' })) },
  ])('valida entrada inválida com Problem Details', async (body) => {
    const r = await post(body).expect(422);
    expect(r.body.code).toBe('VALIDATION_FAILED');
    expect(search).not.toHaveBeenCalled();
  });
  it('não fabrica um link ausente e contextualiza a continuação', async () => {
    const r = await post({
      consulta: { ...input.consulta, pergunta: 'Onde consigo esse requerimento?' },
      historico: [{ role: 'user', content: input.consulta.pergunta }],
    }).expect(201);
    expect(search.mock.calls[0][0].pergunta).toContain(
      'referente ao requerimento para segunda chamada',
    );
    expect(r.body.data.modo_resposta).toBe('verificacao_limitada');
    expect(r.body.data.resposta).toContain('Não encontrei um endereço');
    expect(search.mock.calls[0][0]).not.toHaveProperty('historico');
  });
  it('pede esclarecimento quando não existe referente', async () => {
    const r = await post({ consulta: { pergunta: 'Onde consigo esse requerimento?' } }).expect(201);
    expect(r.body.data.esclarecimento_necessario).toBe(true);
    expect(search).not.toHaveBeenCalled();
  });
  it('não atravessa mudança de assunto', async () => {
    const r = await post({
      consulta: { pergunta: 'Onde consigo esse requerimento?' },
      historico: [
        { role: 'user', content: 'Segunda chamada' },
        { role: 'user', content: 'Como faço estágio?' },
      ],
    }).expect(201);
    expect(r.body.data.esclarecimento_necessario).toBe(true);
  });
  it('mantém fallback no limite provisório, sem chamar geração', async () => {
    search.mockResolvedValue({ ...recovered, distancia_minima: 0.8 });
    const r = await post().expect(201);
    expect(r.body.data.fallback_acionado).toBe(true);
    expect(r.body.data.template_email).toContain('segunda chamada');
    expect(generate).not.toHaveBeenCalled();
  });
  it('geração nula aciona fallback', async () => {
    generate.mockResolvedValue(null);
    expect((await post().expect(201)).body.data.fallback_acionado).toBe(true);
  });
  it.each([
    [
      503,
      new ServiceUnavailableException('Serviço de busca indisponível.'),
      'EXTERNAL_SERVICE_UNAVAILABLE',
    ],
    [504, new GatewayTimeoutException('Tempo limite excedido.'), 'EXTERNAL_SERVICE_TIMEOUT'],
  ] as const)('preserva erro técnico %s sem fingir fallback', async (status, exception, code) => {
    search.mockRejectedValue(exception);
    const r = await post().expect(status);
    expect(r.body.code).toBe(code);
    expect(r.body.data).toBeUndefined();
  });
  it('não expõe endpoint legado sem autenticação nem ingestão', async () => {
    await request(app.getHttpServer()).post('/api/v1/conversa').send(input).expect(404);
    await request(app.getHttpServer())
      .post('/secgrad/api/v1/ingestar')
      .send({ caminho_pdf: 'C:/privado' })
      .expect(404);
  });
  it('responde preflight da origem local permitida', async () => {
    const r = await request(app.getHttpServer())
      .options('/secgrad/api/v1/conversa')
      .set('Origin', 'http://localhost:5173')
      .set('Access-Control-Request-Method', 'POST')
      .expect(204);
    expect(r.headers['access-control-allow-origin']).toBe('http://localhost:5173');
  });
});
