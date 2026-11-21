import { env } from '../../config/env';
import { fetchApi, getApiErrorMessage } from '../../services/api';

export interface Source { arquivo: string; pagina: number; curso: string; trecho?: string }
export interface ChatResult {
  resposta?: string; contexto: string; fontes: Source[]; distancia_minima: number;
  fallback_acionado: boolean; setor_sugerido?: string; template_email?: string;
  modo_resposta?: string; esclarecimento_necessario?: boolean;
}
export interface Message { role: 'user' | 'assistant'; content: string; result?: ChatResult }

function parseResult(value: unknown): ChatResult {
  if (!value || typeof value !== 'object') throw new Error('Resposta inválida da API.');
  const r = value as Record<string, unknown>;
  if (typeof r.contexto !== 'string' || typeof r.fallback_acionado !== 'boolean' ||
      typeof r.distancia_minima !== 'number' || !Number.isFinite(r.distancia_minima) || !Array.isArray(r.fontes) ||
      !r.fontes.every((s: unknown) => {
        if (!s || typeof s !== 'object') return false;
        const f = s as Record<string, unknown>;
        return typeof f.arquivo === 'string' && typeof f.pagina === 'number' && Number.isInteger(f.pagina) && f.pagina >= 1 && typeof f.curso === 'string' && (f.trecho === undefined || typeof f.trecho === 'string');
      }) || (r.resposta !== undefined && typeof r.resposta !== 'string') ||
      (r.fallback_acionado && (typeof r.template_email !== 'string' || typeof r.setor_sugerido !== 'string'))) {
    throw new Error('Resposta inválida da API.');
  }
  return r as unknown as ChatResult;
}

export async function sendQuestion(question: string, course: string, profile: string, history: Message[], signal?: AbortSignal): Promise<ChatResult> {
  if (!question.trim()) throw new Error('Digite uma pergunta.');
  const response = await fetchApi(`${env.apiUrl.replace(/\/$/, '')}/conversa`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(70000)]) : AbortSignal.timeout(70000),
    body: JSON.stringify({
      consulta: { pergunta: question.trim(), curso: course, perfil: profile, top_k: 3 },
      historico: history.filter((m) => m.role === 'user').slice(-10).map(({ content }) => ({ role: 'user', content })),
    }),
  });
  if (!response.ok) throw new Error(await getApiErrorMessage(response, `Não foi possível consultar o servidor (${response.status}).`));
  const envelope = await response.json() as { data?: unknown };
  return parseResult(envelope.data);
}
