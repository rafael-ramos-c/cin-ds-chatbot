# Correção posterior ao pacote acadêmico — texto dos PDFs

Problema observado em teste manual: PPCs com uma palavra por linha e busca recuperando passagens sobre acessibilidade para pergunta sobre estágio.

Alterações: normalização conservadora antes do chunking quando uma página tem pelo menos 20 linhas e 80% delas têm até duas palavras; palavras são preservadas, separadores de parágrafo e artigos recompostos. Perguntas com menção explícita a estágio recebem restrição textual temática no ChromaDB, mantendo filtros de curso/perfil, consulta original, distâncias e limiar. Interface informa a normalização e os limites da recuperação.

Validação: 27 testes atuais de IA, 21 testes V2 históricos e 12 testes do cliente UI aprovados. Reingestão local: 21/21 documentos; 6779 trechos. Consulta real em consulta.txt. O trecho de acessibilidade deixou o top 3, mas os resultados ainda não garantem responder precisamente quando o aluno pode iniciar o estágio. A heurística temática é limitada aos termos previstos e pode reduzir a recuperação; deve ser ampliada/avaliada com benchmark antes de alegar precisão geral. Tabelas e páginas mistas não são reconstruídas geometricamente. Não há LLM real; mock preservado.

Os PDFs, benchmarks, hashes e ZIP acadêmicos anteriores não foram reescritos: descrevem a revisão anterior. Este ajuste funcional é posterior e não deve ser apresentado como se integrasse suas medições históricas. Para entregar este estado novo, publicar a correção separadamente e atualizar o pacote de entrega e verificações que dependam de hashes da revisão atual.

Para ver a correção na interface, reiniciar os três serviços conforme README e limpar o histórico antigo do chat. O ChromaDB local já foi atualizado; outros computadores precisam reingerir após atualizar o código. Não versionar a pasta chroma_db.
