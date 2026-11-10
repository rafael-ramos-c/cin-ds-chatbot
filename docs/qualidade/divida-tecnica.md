# Registro de dívida técnica - revisão de 09/11/2026

Registro inicial de Ricardo complementado por Rafael com evidências de IA/backend.
Prazo de conferência interna: 13/11/2026; entrega informada: 15/11 às 23h59.
Responsáveis indicam a divisão de trabalho, não aprovação individual retrospectiva.

| ID | Problema / impacto | Prioridade | Responsável | Situação | Plano / prazo | Critério de conclusão e evidência |
| --- | --- | --- | --- | --- | --- | --- |
| DATA-02 | PPCs ausentes da base curricular | Alta | Ricardo / Rafael | Incorporação inicial resolvida; OCR em validação separada | Documentos e metadados publicados; reingestão após atualização | Sete PPCs no catálogo e consultas isoladas por curso/perfil. Auditoria de 07/11 em ../testes/validacao-ppcs/auditoria-final.json; rodada pós-OCR: 21 documentos, 6.811 trechos e sete pares conferidos, sem divergências, no índice abaixo. Não significa OCR integral. |
| DATA-01 | Duplicação em data/raw/ e ai-service/data/ permite editar versão errada | Alta | Ricardo / Rafael | Aberta; fonte canônica já definida | Ricardo conferir dependências antes de remover/arquivar legado; 13/11 | Somente uma fonte documental mantida ou legado explicitamente arquivado e referências atualizadas. config.py já aponta data/raw; as cópias ainda existem. |
| DATA-03 | EC anterior, página 22, continua sem extração; OCR pode introduzir erro | Alta | Ricardo | Parcial: quatro de cinco páginas com texto | Revisar EC22 e fidelidade das quatro páginas; corrigir OCR ou justificar exclusão; 13/11 | Todas as páginas relevantes extraídas e conferidas, ou exclusões justificadas por conteúdo. ocr-comparacao.json registra estado atual. |
| IA-REF-02 | Validação vetorial misturada à formatação/manutenção da busca | Média | Rafael | Refatorada | Extract Function concluída no commit 8e2f8f6 | Mesma V2 21/21 antes/depois; ver IA-REF-02-relatorio.md e manifestos. |
| BACK-REF-01 | Condicionais consecutivas repetem decisão e retorno SecGrad | Média | Victor | Refatorada | Consolidate Conditional Expression no commit f7a067f | Mesma V2 105/105 antes/depois; ver BACK-REF-01-relatorio.md. |
| QA-01 | Limiar 0,8 sem calibração documentada pode aceitar assunto externo | Alta | Eric, com Rafael / Victor | Aberta | Medir perguntas positivas/negativas e conjunto de validação; justificar limiar; 13/11 | Benchmark com fontes esperadas, erros e decisão registrada. Um caso de carburador já recuperou contexto; não calibrar por apenas uma pergunta. |
| UI-01 | Contexto priorizado sobre resposta oculta aviso de simulação | Alta | Eric | Aberta na revisão conferida | Revisar apresentação e caracterizar comportamento antes da terceira refatoração; 13/11 | Resposta/contexto/fontes identificados sem confundir mock com resposta acadêmica; evidência de UI e testes. Não marcar como refatorada sem V2 antes/depois. |
| DOC-01 | Evidências históricas do backend não contêm prompt V2 integral e snapshot exato | Média | Rafael / Victor | Limitação documental aberta | Recuperar somente registros reais; se ausentes, manter ressalva explícita; 13/11 | Referências históricas verificáveis ou indisponibilidade documentada, sem reconstruir conversa e atribuir data antiga. Ver ../testes/llm-log.md. |

## Escopo e achados descartados

Foram examinados ingestão/configuração/retriever, retorno HTTP e orquestração,
cliente UI, catálogo, PDFs e evidências V1/V2. O registro distingue dívida de
manutenção, lacuna de validação e limitação documental; não são oito refatorações.
React, Keycloak/LDAP, Docker e provedor real de LLM são requisitos gerais pendentes,
não foram contados como smells nem como refatorações concluídas.

BACK-COR-URL-01 foi correção funcional coberta por regressões, não terceira
refatoração. Adicionar avisos de páginas sem texto e roteiro PowerShell também não
foi contado como refatoração formal. Terceiro item de Eric permanece pendente.

## Evidências da atualização

[Validação pós-OCR](../testes/validacao-pos-ocr-20261109/README.md), com hashes,
comparação dos PDFs, reingestão, auditoria e ensaio separado dos serviços.
O [log de análise](log-analise.md) distingue relato de execução de verificação
independente. Itens abertos exigem revisão dos responsáveis antes da entrega.
