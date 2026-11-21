import { createZodDto } from 'nestjs-zod';
import { z } from 'zod';

const field = z.string().trim().min(1).max(2000);
const normalize = (s: string) =>
  s.toLowerCase().normalize('NFKD').replace(/\p{M}/gu, '').replace(/\s+/g, ' ').trim();
const courses: Record<string, string> = {
  cc: 'CC',
  'ciencia da computacao': 'CC',
  ec: 'EC',
  'engenharia da computacao': 'EC',
  si: 'SI',
  'sistemas de informacao': 'SI',
  'sistemas de informacoes': 'SI',
  ia: 'IA',
  'inteligencia artificial': 'IA',
  geral: 'Geral',
  todos: 'Geral',
};
const profiles: Record<string, string> = {
  novo: 'novo',
  vigente: 'novo',
  'perfil novo': 'novo',
  'perfil vigente': 'novo',
  'perfil novo / vigente': 'novo',
  'unico perfil': 'novo',
  unico: 'novo',
  anterior: 'anterior',
  antigo: 'anterior',
  'perfil antigo': 'anterior',
  'perfil anterior': 'anterior',
  todos: 'Todos',
  ambos: 'Todos',
};
function identifier(aliases: Record<string, string>, label: string) {
  return z
    .string()
    .trim()
    .min(1)
    .max(100)
    .refine((v) => Object.hasOwn(aliases, normalize(v)), `${label} desconhecido.`)
    .transform((v) => aliases[normalize(v)]);
}
const query = z
  .object({
    pergunta: field,
    curso: identifier(courses, 'Curso').optional(),
    perfil: identifier(profiles, 'Perfil curricular').optional(),
    top_k: z.number().int().min(1).max(10).optional(),
  })
  .strict()
  .superRefine((query, ctx) => {
    if (query.curso === 'IA' && query.perfil === 'anterior')
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['perfil'],
        message: 'Inteligência Artificial possui perfil único.',
      });
  });

export const ConversationSchema = z
  .object({
    consulta: query,
    dados_email: z
      .object({
        nome: field.optional(),
        matricula: field.optional(),
        assunto: field.optional(),
        resumo: field.optional(),
      })
      .strict()
      .optional(),
    // Histórico de perguntas usado apenas para resolver referências limitadas.
    // Não é armazenamento permanente nem segue ao provedor de IA.
    historico: z
      .array(z.object({ role: z.literal('user'), content: field }).strict())
      .max(10)
      .optional(),
  })
  .strict();

export class ConversationDto extends createZodDto(ConversationSchema) {}
