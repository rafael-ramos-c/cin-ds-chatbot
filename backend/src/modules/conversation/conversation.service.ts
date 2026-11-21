import { Inject, Injectable } from '@nestjs/common';
import { OrchestrationService } from '../../orchestration/orchestration.service';
import type { ConversationDto } from './conversation.dto';

const normalize = (s: string) => s.toLowerCase().normalize('NFKD').replace(/\p{M}/gu, '');
const reference = (s: string) => /\b(esse|este|desse|deste|isso|ele)\b/.test(normalize(s));

export function contextualize(
  question: string,
  history: ConversationDto['historico'] = [],
): string | null {
  const n = normalize(question);
  if (!(reference(question) && /\b(requerimento|formulario|documento|isso|ele)\b/.test(n)))
    return question;
  for (const previous of [...history].slice(-3).reverse()) {
    if (/segunda chamada|2ª chamada|2a chamada/.test(normalize(previous.content))) {
      return `${question} (referente ao requerimento para segunda chamada de prova)`;
    }
    if (!reference(previous.content)) break;
  }
  return null;
}

export interface SourceWithExcerpt {
  arquivo: string;
  pagina: number;
  curso: string;
  trecho: string;
}

export function associateExcerpts(
  context: string,
  sources: Omit<SourceWithExcerpt, 'trecho'>[],
): SourceWithExcerpt[] {
  const matches = [
    ...context.matchAll(/(?:^|\n\n---\n\n)\[Documento: (.*?) \| Pág\. (\d+) \| Curso: (.*?)\]\n/g),
  ];
  return sources.map((source, i) => {
    const m = matches[i];
    const matchesSource =
      m && m[1] === source.arquivo && Number(m[2]) === source.pagina && m[3] === source.curso;
    const trecho = matchesSource
      ? context.slice(m.index + m[0].length, matches[i + 1]?.index ?? context.length).trim()
      : '';
    return { ...source, trecho };
  });
}

@Injectable()
export class ConversationService {
  constructor(@Inject(OrchestrationService) private readonly orchestration: OrchestrationService) {}

  async converse(input: ConversationDto) {
    const question = contextualize(input.consulta.pergunta, input.historico);
    if (question === null)
      return {
        resposta:
          'A qual requerimento ou formulário você se refere? Informe o procedimento, por exemplo, segunda chamada de prova.',
        fontes: [],
        contexto: '',
        distancia_minima: 1,
        fallback_acionado: false,
        esclarecimento_necessario: true,
        modo_resposta: 'esclarecimento',
      };
    const result = await this.orchestration.processar({
      ...input,
      consulta: { ...input.consulta, pergunta: question },
    });
    const fontes = associateExcerpts(result.contexto, result.fontes);
    if (result.fallback_acionado) return { ...result, fontes, modo_resposta: 'fallback' };
    const simulated = result.resposta.includes('[SIMULAÇÃO DE INTEGRAÇÃO');
    const asksAddress =
      /\b(onde|link|endereco|baixar|download)\b/.test(normalize(question)) &&
      /\b(requerimento|formulario)\b/.test(normalize(question));
    if (simulated && asksAddress && !fontes.some((s) => /https?:\/\/\S+/i.test(s.trecho)))
      return {
        ...result,
        fontes,
        modo_resposta: 'verificacao_limitada',
        resposta:
          'Não encontrei um endereço para obter esse requerimento nos trechos consultados. A referência ao formulário, sozinha, não informa onde baixá-lo. Confirme o endereço com a secretaria ou coordenação do curso.\n\n[VERIFICAÇÃO DOCUMENTAL LIMITADA — SEM GERAÇÃO POR LLM]',
      };
    return { ...result, fontes, modo_resposta: simulated ? 'simulacao' : 'geracao' };
  }
}
