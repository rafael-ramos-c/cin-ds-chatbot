# Auditoria de aderência aos roteiros - 10/11/2026

Conferência de evidências, não estimativa de nota ou certificado de aprovação.

| Critério | Evidência | Situação / limite |
| --- | --- | --- |
| Matriz anterior à V1 | matriz-rastreabilidade.md e commit 97aa72f | Registro existente. Elaboração assistida autorizada conforme relato do usuário; sem atas inventadas |
| V1 preservada | testes v1-llm e pacote original de Victor | Conteúdo preservado; falhas não apagadas |
| Log de interações/modelo | llm-log.md e fontes integrais da IA/backend | Lacunas históricas de prompt V2 e snapshot exato não preenchidas retrospectivamente |
| V1/V2 no mesmo escopo | us01-controlado e comparacao-v1-v2 do backend | Indicadores conferidos; não misturar escopo ampliado com original |
| Requisitos, partições e limites | matriz e inventario-consolidado | Contagens explícitas; presença de oráculo não significa conformidade universal |
| Aumento de branches | IA 76,19% -> 97,62%; backend 100% -> 100% | Teto declarado. Não degradar V1 ou trocar denominador para fabricar aumento; alinhar interpretação com monitor se necessário |
| Três refatorações com V2 da Parte 1 | BACK-REF-01, IA-REF-02 e IA-REF-04 | Antes/depois e V2 acadêmicas preservadas. BACK-REF-03 é complementar |
| Commits por item | f7a067f, 8e2f8f6, c0f7116; complemento 27d0d9b | Novos commits locais devem ser publicados sem squash |
| Dívida com local, categoria e efeito | qualidade/divida-tecnica.md e documentos por ID | Itens de projeto separados de defeitos e limitações; escopo e descartes descritos |
| Comparação de formas de análise | PDF e log-analise.md | Autoria pessoa/LLM não foi isolada experimentalmente; ferramentas não certificam projeto |
| Limite dos PDFs | reforco-20261110: cinco e três páginas | Renderização conferida, links do índice verificados |
| Reprodução | Comandos, versões, JSON, HTML e snapshots | Instalar dependências e preparar banco conforme manual; não são empacotados |
| Fallback semântico | Benchmark de 25 casos e dados brutos | Falhas reais mantidas em QA-01; não declarar limiar calibrado ou LLM real |
| Revisão e envio | Rafael e grupo | Ler PDFs, conferir entendimento, publicar commits e anexar no Classroom |

## Melhoria desta rodada

O risco de depender somente da regressão corrente para cumprir o terceiro item
foi mitigado por uma nova refatoração medida diretamente com a V2 da Parte 1.
Não se alterou a história para melhorar a aparência da entrega anterior.

## Limites que edição documental não resolve

O prompt V2 integral do backend e o snapshot exato não estão disponíveis no
material recebido. Somente registros originais recuperados podem suprir isso.
O teto de 100% de branches não cresce no mesmo recorte; a ressalva será avaliada
pelo docente. Leitura e confirmação humana dos diagnósticos não são substituídas
por assinatura do assistente. Esses limites permanecem explícitos.
