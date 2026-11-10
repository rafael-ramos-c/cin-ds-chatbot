# Dívida técnica e pendências de qualidade - fechamento de 10/11/2026

Rafael assumiu o fechamento de Victor e Eric por solicitação do grupo. Itens
registrados por inspeção assistida e resultados de ferramentas; a leitura final
pelos integrantes não é substituída por assinaturas ou aprovações inventadas.
Prazo interno de revisão: 13/11; entrega: 15/11 às 23h59 (Fortaleza).

## Itens de projeto e manutenção

| ID / local | Problema, categoria e consequência | Identificação | Situação / plano | Evidência / critério |
| --- | --- | --- | --- | --- |
| BACK-REF-01 / backend/src/orchestration/fallback.service.ts, identificarSetor | Duplicated Code e integridade conceitual: decisões adjacentes repetem destino e dificultam mudar palavras-chave sem divergência | Leitura do fluxo com apoio de LLM, registro histórico de Victor | Refatorado por Consolidate Conditional Expression, f7a067f | V2 histórica 105/105 antes/depois; BACK-REF-01-relatorio.md |
| IA-REF-02 / ai-service/src/retriever.py, buscar_contexto | Long Method, coesão e orientação SRP: integridade vetorial misturada a formatação e consulta | Inspeção assistida em etapa anterior | Refatorado por Extract Function, 8e2f8f6 | Mesma V2 US-01 21/21 antes/depois; IA-REF-02-relatorio.md |
| BACK-REF-03 / backend/src/ai-service/ai-service.service.ts, getEndpoint | Coesão de método, Long Method relativo ao fluxo: política de origem ocupa a construção de rota e tratamento HTTP, dificultando localizar a regra | Inspeção do módulo neste chat, apoio de LLM; descarta alegação de remover todo acoplamento da classe | Refatorado por Extract Function, 27d0d9b; congelamento 2a33101 | V2 de regressão corrente 256/256 antes/depois, hashes iguais; BACK-REF-03-relatorio.md. Não reatribuir à baseline V2 antiga |
| DATA-01 / data/raw/ e ai-service/data/, config.py | Duplicação de dados e integridade conceitual: duas cópias podem ser editadas em paralelo e divergir | Inspeção do histórico e diretórios | Aberta, mitigada por data/raw canônico; Ricardo/Rafael revisam dependências antes de arquivar legado, próximo ciclo | Nenhum arquivo foi removido; concluir com origem única ou legado arquivado e referências atualizadas |
| API-01 / src/ui/api_client.py, extrair_trechos e contrato contexto | Acoplamento ao formato textual e information hiding frágil: UI depende de cabeçalho da recuperação | Leitura assistida durante correção de fontes | Aberta, mitigada por associação estrita de arquivo/página/curso; Rafael, próximo ciclo | Evoluir contrato para trechos estruturados com compatibilidade e testes ponta a ponta; hoje omite citação quando não consegue associar, sem inventar texto |
| UI-DUP-01 / app.py, histórico e resposta imediata | Duplicated Code: renderização das fontes aparece em dois blocos, tornando ajustes visuais propensos a divergência | Inspeção assistida dos dois loops | Aberta; Rafael assumiu Eric, próximo ciclo | Caracterizar UI e extrair componente mantendo comportamento; não contou como terceira refatoração |

## Defeitos, validação e documentação (não apresentados como smells)

| ID / local | Impacto e situação | Evidência / plano |
| --- | --- | --- |
| DATA-02 / catálogo e sete PPCs | Incorporação resolvida; 21 documentos e 6.811 trechos conferidos | ../testes/validacao-pos-ocr-20261109/auditoria-final.json. Arquivos não mudaram nesta rodada; hashes conferidos |
| DATA-03 / EC anterior 22 e quatro páginas SI | EC22 sem extração justificada como contracapa administrativa; OCR de SI relatado como conferido por Ricardo | Imagem EC22 e relato distinguido no log. Não declarar OCR da página escura bem-sucedido, nem apagar a página; não inferir revisão semântica integral por pypdf |
| UI-01 / cliente e expansor | Corrigida prioridade da resposta e citação literal. Legenda de página deixou de ser apresentada como citação | Commit funcional 0b334a7; 12 testes UI e AppTest com HTTP real. Não é refatoração formal |
| QA-01 / recuperação e limiar | Aberta, alta: aceita perguntas externas; 0,8 não está calibrado | Benchmark final 25 casos: dez aceitações externas com 0,8 e sete com 0,5. Rafael/equipe, próximo ciclo: corpus/embeddings, avaliação de escopo e conjunto independente; critério e alvo devem ser definidos antes de calibrar |
| BACK-COR-THRESHOLD-01 / fallback.config.ts | Resolvida divergência 0,5 versus contrato provisório 0,8 | Restaurado 0,8 sem modificar testes; 256/256 no Node 24. Não significa limiar semanticamente ideal |
| DOC-01 / histórico LLM backend | Limitação documental explícita: snapshot exato e prompt V2 integral indisponíveis | Não reconstruir conversa e atribuir data antiga. ../testes/llm-log.md e PDF crítico preservam a ressalva |

## Escopo procurado e falsos enquadramentos descartados

Revisados fallback, orquestração, cliente HTTP, origem de URL, retriever,
metadados, sincronização da ingestão, interface e catálogo. Há seis itens de
projeto/manutenção neste registro; não se completou uma meta numérica com
problemas inventados. As tabelas de validação não são seis novos code smells.

Não foram confirmadas violações de todos os princípios SOLID. Validar dados
externos na borda HTTP é necessário; não é defeito por si só. Timeout existente
não foi contado como nova refatoração. Corrigir limiar, exibir trecho e adicionar
avisos OCR são mudanças funcionais, separadas dos três commits de refatoração.

Oxlint foi executado (dois avisos preexistentes de stringificação em testes,
nenhum erro). Não houve Sonar/jscpd nem medida automática de smells. Cobertura
não comprova boa arquitetura. React, Keycloak/LDAP, Docker Compose/Swarm e LLM
real são requisitos gerais ainda pendentes, não contados como refatorações.
