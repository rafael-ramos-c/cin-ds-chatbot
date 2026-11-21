import { afterEach, describe, expect, it, vi } from 'vitest';
import { sendQuestion } from './chat.service';
import { setAuthToken, setRefreshTokenFn } from '../../services/api';

const data = { contexto: 'Texto', fontes: [{ arquivo: 'norma.pdf', pagina: 1, curso: 'IA', trecho: 'Texto' }], distancia_minima: 0.2, fallback_acionado: false, resposta: '[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]' };
afterEach(() => { vi.unstubAllGlobals(); setAuthToken(null); setRefreshTokenFn(null); });
describe('Cliente da conversa autenticada', () => {
  it('envia Bearer, filtros e apenas perguntas anteriores; lê data', async () => {
    const fetch = vi.fn().mockResolvedValue(Response.json({ data })); vi.stubGlobal('fetch', fetch); setAuthToken('token-local');
    const r = await sendQuestion(' Pergunta? ', 'IA', 'unico', [{ role: 'user', content: 'Anterior' }, { role: 'assistant', content: 'Resposta privada' }]);
    expect(r).toEqual(data);
    expect(String(fetch.mock.calls[0][0])).toContain('/secgrad/api/v1/conversa');
    const options = fetch.mock.calls[0][1]; expect(options.headers.get('Authorization')).toBe('Bearer token-local');
    expect(JSON.parse(options.body)).toEqual({ consulta: { pergunta: 'Pergunta?', curso: 'IA', perfil: 'unico', top_k: 3 }, historico: [{ role: 'user', content: 'Anterior' }] });
  });
  it('mostra detail do Problem Details e não troca erro por resposta simulada', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(Response.json({ detail: 'Serviço de geração indisponível.' }, { status: 503 })));
    await expect(sendQuestion('P', 'IA', 'unico', [])).rejects.toThrow('Serviço de geração indisponível.');
  });
  it.each([{ data: {} }, data, { data: { ...data, fontes: [{ arquivo: 'x', pagina: 0, curso: 'IA' }] } }])('rejeita resposta incompatível', async (body) => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(Response.json(body)));
    await expect(sendQuestion('P', 'IA', 'unico', [])).rejects.toThrow('Resposta inválida');
  });
  it('não envia pergunta em branco', async () => {
    const fetch = vi.fn(); vi.stubGlobal('fetch', fetch);
    await expect(sendQuestion(' ', 'IA', 'unico', [])).rejects.toThrow('Digite uma pergunta'); expect(fetch).not.toHaveBeenCalled();
  });
});
