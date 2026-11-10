# Entrega da Sprint 3 - Chatbot SecGrad / CInCoders

Fechamento técnico em 10/11/2026 por Rafael, assumindo as etapas finais de Victor
e Eric. Entrega informada: 15/11/2026 às 23h59, sem apresentação. Este índice
organiza o material; não é declaração de aprovação da professora ou do grupo.

## Arquivos principais para entregar

1. [Análise crítica, cinco páginas](testes/analise-critica-sprint3-final-20261110.pdf).
2. [Refatorações, três páginas e três itens](qualidade/relatorio-refatoracoes-sprint3-final-20261110.pdf).
3. [Matriz final de rastreabilidade](testes/matriz-rastreabilidade.md).
4. [Log da LLM e referências às interações originais](testes/llm-log.md).
5. [Dívidas técnicas](qualidade/divida-tecnica.md) e [log de análise](qualidade/log-analise.md).
6. [Evidências finais e reprodução](testes/fechamento-final-20261110/README.md),
   [benchmark completo](testes/fechamento-final-20261110/BENCHMARK.md),
   [terceira refatoração](qualidade/BACK-REF-03-relatorio.md).

Não enviar apenas os dois PDFs: matriz, log, código de testes, HTMLs e evidências
são entregas complementares dos roteiros e acompanham o pacote.

## Testes acadêmicos preservados e coberturas

- IA V1: ai-service/tests/v1-llm/; IA V2: ai-service/tests/v2/.
- IA HTML controlado: [V1](testes/relatorios/us01-controlado/v1/html/index.html) e
  [V2](testes/relatorios/us01-controlado/v2/html/index.html).
- Backend V1 original: [geração e testes](testes/evidencias-backend/01_V1/geracao/),
  [HTML](testes/evidencias-backend/01_V1/execucao/coverage/index.html).
- Backend V2 original: backend/test/sprint3-v2/; [HTML](testes/evidencias-backend/02_V2/execucao/coverage/index.html).
- A produção histórica necessária à reprodução não é a main atual; ver scripts
  e baselines em testes/CONSOLIDACAO-SPRINT3.md e registros de Victor.
- HTML da nova refatoração: [antes](qualidade/BACK-REF-03-evidencias/antes/coverage/index.html)
  e [depois](qualidade/BACK-REF-03-evidencias/depois/coverage/index.html).

## Commits que devem permanecer identificáveis

- BACK-REF-01: f7a067fb7886d1b68621ca57af42cf051dfe02a1 (histórico de Victor).
- IA-REF-02: 8e2f8f6 (histórico de Rafael).
- Correções funcionais atuais: 0b334a7 (limiar e fonte literal; não refatoração).
- Congelamento antes de BACK-REF-03: 2a33101.
- BACK-REF-03: 27d0d9bd4a97556fab53b4d4a3762279cf6f8b8e.

Publicar a branch preservando esses commits. Não usar squash se isso apagar a
separação exigida entre a correção funcional, o registro anterior e o item refatorado.
O código não foi enviado automaticamente ao GitHub.

## Ressalvas que fazem parte da análise

- Geração é mock, não LLM real. O benchmark avalia recuperação e decisão de
  fallback; não avalia correção de uma resposta acadêmica gerada.
- Limiar 0,8 permanece provisório. A amostra de 25 perguntas encontrou dez
  aceitações fora do escopo; 0,5 ainda teve sete. Essa dívida não foi escondida
  para declarar o produto perfeito. A planilha original permanece intacta.
- EC22 é contracapa com etiqueta administrativa; exclusão justificada e imagem
  preservada. Isso não equivale a OCR bem-sucedido dessa página. Ricardo relatou
  conferência local do texto de SI; não foi inventada uma nova inspeção humana.
- O prompt original preservado do backend não explicita todos os critérios e
  técnicas pedidos. O prompt integral V2 e snapshot exato não foram recuperados.
  Mantém-se a limitação histórica; não há nova V1 retroativamente datada.
- A V1 do backend já tinha 100% de branches no escopo original: o aumento estrito
  da meta não ocorre nesse recorte. O PDF explica teto e ganho funcional, sem
  trocar denominadores. Se houver exigência de interpretação, esclarecer com o
  monitor; não se presume dispensa dessa meta pela professora.
- BACK-REF-03 utiliza V2 de regressão corrente, com proteção de URL e geração;
  não é execução dos 105 testes antigos sobre a produção atual. O relatório
  distingue as camadas. Nenhuma suíte antiga foi alterada para fabricar aprovação.
- O uso assistido da matriz foi autorizado e aprovado conforme informado por
  Rafael; não existem atas/assinaturas criadas por nós para substituir essa informação.

## Antes de enviar à professora

Rafael deve ler os dois PDFs, conferir se o texto representa o trabalho do grupo,
publicar os commits e integrar a branch. Conferir o destino de anexos da atividade
e enviar os arquivos exigidos, incluindo apêndices. Não é necessário esperar nova
implementação de Eric ou Victor para organizar essa entrega; pendências reais de
produto ficaram registradas no backlog. A revisão humana e o envio não foram feitos
pelo assistente.

React, Keycloak/LDAP, Docker Compose/Swarm e provedor real de LLM são requisitos
gerais do projeto ainda pendentes de comprovação. Esta entrega de qualidade e
testes não os apresenta como implementados.
