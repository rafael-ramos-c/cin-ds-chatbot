# Evidências finais da Sprint 3 - 10/11/2026

Rafael assumiu as etapas restantes de Victor e Eric. Base inicial cd583e4.
Node 24.22.1, ambiente Python do projeto, corpus real e geração mock.

## Alterações e sequência verificável

1. Correção funcional em 0b334a7: restaura padrão provisório 0,8 e mostra trechos
literais da API na UI, associando arquivo/página/curso. Contexto não aparece como
se fosse resposta gerada. Acrescenta 12 testes de regressão UI.
2. Congelamento 2a33101: diagnóstico BACK-REF-03, configuração e evidências antes.
3. Refatoração isolada 27d0d9b: Extract Function para política de origem do AiService.
Mesma suíte V2 de regressão corrente 256/256 antes/depois, hashes conferidos e
cobertura do mesmo arquivo. Não é nova execução da V2 acadêmica histórica.
4. Benchmark com casos predefinidos e medições reais de 25 perguntas comparando
0,8 e 0,5. AppTest valida a UI com chamadas HTTP reais. Ver BENCHMARK.md.
5. Incorporação da justificativa EC22: contracapa escura com etiqueta administrativa,
sem conteúdo curricular corrido. Imagem ec-pagina-22.png, página mantida no PDF.
Ricardo relatou conferência local do OCR de quatro páginas SI; aqui não houve
nova execução de OCR nem alteração de PDFs-fonte ou base vetorial.
6. PDFs finais de cinco e três páginas, índice de entrega, governança e log revistos.

## Resultados atuais

| Verificação | Resultado |
| --- | --- |
| Backend unitário / antes e depois | 256/256 |
| Seleção de geração citada por Eric | 52/52, subconjunto dos 256 |
| E2e comum | 34 aprovados, dois opt-in pulados nessa chamada |
| E2e opt-in em serviços reais | Dois aprovados separadamente |
| Ensaio HTTP real | Dez cenários aprovados |
| IA regressão / V2 US-01 | 20/20 e 21/21 |
| Cliente UI | 12/12 |
| Interface AppTest | Aviso mock, página, trecho literal, histórico e minuta em cenário 0,5 |
| Nest build | Exit 0 |
| Oxlint | Exit 0; dois avisos preexistentes em testes |
| Corpus auditado anterior | 21 documentos, 6.811 trechos; hashes dos arquivos atuais conferidos |

Arquivos de execução: backend-unitarios-corrigidos.json (antes da extração),
backend-e2e.json, geracao-52.json, ia-regressao.txt, ia-v2.txt, ui-unitarios.txt,
servicos-reais/ e ../../qualidade/BACK-REF-03-evidencias/ (ver índice principal).
A primeira revisão com 254/256 está preservada em ../revisao-eric-20261110/.
Ela não é o resultado corrente após restaurar 0,8.

## Benchmark e limitações

Resultado canônico: benchmark-entrega/benchmark.json. Casos: benchmark-casos.json,
definidos antes das execuções. A primeira tentativa benchmark-real/ usou nomes
esperados de PPC em maiúsculas, produzindo sete falsas divergências no oráculo.
A lista inicial está preservada em benchmark-casos-oraculo-inicial.json. Corrigiu-se
somente a capitalização e repetiu-se em benchmark-final/. A rodada de entrega
acrescenta verificação visual da minuta com 0,5, mantendo as perguntas e expectativas.

No padrão 0,8: 15/25 decisões conforme e dez aceitações externas indevidas. Com
0,5: 18/25 e sete aceitações externas indevidas. Nenhuma recusa dos 15 casos internos.
Os sete controles recuperaram o PPC esperado. Isso não comprova resposta acadêmica:
a geração é mock e vários nomes de fontes da planilha Sprint 1 são legados.

Não se selecionou limiar ideal, não se ocultaram falhas e não se ajustaram perguntas
para obter nota maior. QA-01 fica aberta. AppTest não é inspeção de pixels em
navegador. Os processos temporários foram encerrados. Nenhum e-mail foi enviado.

## Reprodução

Na raiz: ambiente Python do projeto ativo; Node.js 24; dependências instaladas.

```powershell
cd backend
npm ci
npm run build
npm test
npm run test:e2e
npm run lint
cd ..
python -m unittest discover -s tests/ui -v
cd ai-service
python -m unittest discover -s tests -v
python -m unittest discover -s tests/v2 -p test_busca_v2.py -v
cd ..
python scripts/benchmark_sprint3.py --casos docs/testes/fechamento-final-20261110/benchmark-casos.json --saida docs/testes/benchmark-novo
python backend/scripts/verificar-integracao-real.py --saida docs/testes/integracao-nova
```

Os dois últimos criam/encerram seus processos em portas livres. Não usar pasta de
resultado existente. Antes do benchmark, preparar ChromaDB conforme manual; não
instalar dependências ou reingerir enquanto outro processo usa a base. O teste
não requer chave de provedor de LLM. Cada computador tem seu próprio banco local.

Cobertura de BACK-REF-03: em backend/, definir BACK_REF03_EVIDENCE_DIR apontando
para uma pasta NOVA e executar `node node_modules/vitest/vitest.mjs run --config
vitest.back-ref03.config.mts --coverage`. Não sobrescrever antes/depois históricos.

## Entrega e revisão

Leia ../../ENTREGA-SPRINT3.md. PDFs finais em docs/testes/ e docs/qualidade/.
O manifesto final contém hashes, contagens, testes preservados e páginas dos PDFs.
O ZIP de entrega inclui documentos complementares, fontes de testes, código e
histórico/diff, sem venv, node_modules, .git ou ChromaDB local. Dependências devem
ser instaladas para reproduzir, e baselines antigas requerem o histórico Git remoto.

A revisão final pelo grupo e o envio à atividade não são efetuados pelo assistente.
Ressalvas históricas de prompt e teto de branches continuam explícitas no PDF.
