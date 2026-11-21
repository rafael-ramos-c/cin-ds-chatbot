import { BadRequestException } from '@nestjs/common';
import { FallbackService } from './fallback.service';
import type { DadosEmailFallback } from './orchestration.types';

const service = new FallbackService();

describe('FallbackService', () => {
  it.each([
    ['ESTÁGIO obrigatório', 'SecGrad'],
    ['estagio', 'SecGrad'],
    ['Requerimento', 'SecGrad'],
    ['Dispensa', 'SecGrad'],
    ['segunda chamada', 'SecGrad'],
    ['Apoio pedagógico', 'NEAP'],
    ['apoio pedagogico', 'NEAP'],
    ['PÓS-GRADUAÇÃO', 'Secretaria de Pós-Graduação'],
    ['pos-graduacao', 'Secretaria de Pós-Graduação'],
    ['pós graduação', 'Secretaria de Pós-Graduação'],
    ['Dúvida geral', 'SecGrad'],
    ['estágio pedagógico', 'SecGrad'],
    ['pedagógico pós-graduação', 'NEAP'],
  ])('sugere o setor para %s', (assunto, setor) => {
    expect(service.identificarSetor(assunto)).toBe(setor);
  });

  it('gera template de texto com os dados informados', () => {
    const email = service.gerarEmail({
      consulta: {
        pergunta: 'Como solicitar apoio?',
        curso: 'CC',
        perfil: '2023',
      },
      dados_email: {
        nome: 'Ana',
        matricula: '123',
        assunto: 'Apoio pedagógico',
        resumo: 'Preciso de orientação.',
      },
    });
    expect(email.setor_sugerido).toBe('NEAP');
    expect(email.template_email).toBe(`Assunto: Apoio pedagógico

Olá,

Meu nome é Ana, matrícula 123, aluno(a) do curso de CC, perfil curricular 2023.

Estou entrando em contato sobre: Apoio pedagógico.

Resumo da situação:
Preciso de orientação.

Minha dúvida é:
Como solicitar apoio?

Setor sugerido:
NEAP

Atenciosamente,
Ana`);
  });

  it('usa campos editáveis quando não há dados pessoais e pergunta como assunto', () => {
    const email = service.gerarEmail({ consulta: { pergunta: 'Dispensa?' } });
    expect(email.template_email).toContain('Assunto: Dispensa?');
    for (const field of [
      '[Nome]',
      '[Matrícula]',
      '[Curso]',
      '[Perfil curricular]',
      '[Resumo da situação]',
    ]) {
      expect(email.template_email).toContain(field);
    }
    expect(email.template_email).not.toMatch(/undefined|null/);
  });

  it.each([
    null,
    [],
    'invalid',
    { nome: 123 },
    { matricula: null },
  ])('rejeita dados de e-mail inválidos %j', (dados) => {
    expect(() => service.validarDadosEmail(dados as DadosEmailFallback)).toThrow(
      BadRequestException,
    );
  });
});
