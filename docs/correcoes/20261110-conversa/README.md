# Revisão conversacional — 10/11/2026

## Resultado e limites

O histórico era apenas visual. Agora `src/ui/conversation.py` contextualiza referências curtas a formulário quando o último assunto explícito é segunda chamada, com limite de três mensagens de usuário; não cruza mudança explícita de assunto. Sem antecedente conhecido pede esclarecimento sem consultar a API. Não é memória geral nem reescrita por LLM. `app.py` limpa a conversa ao trocar curso/perfil. A pergunta visível é preservada; a consulta inclui a referência explícita.

`src/ui/api_client.py` detecta pedido de endereço de formulário. Se não há URL HTTP(S) nos trechos associados e não houve fallback do backend, informa ausência nos trechos consultados; não afirma que o formulário inexiste na instituição. Não inventa link. Quando há URL, preserva a saída existente, sem certificar destino ou pertinência do endereço. Erro HTTP continua erro técnico. Mensagem documental local é identificada, não apresentada como geração de LLM.

O retriever limita perguntas explicitamente sobre estágio ou segunda chamada a trechos com termos previstos. Curso/perfil continuam filtrados. Isto reduz ruído, mas pode perder documentos com grafias distintas e não resolve ranking, ambiguidade de TG/prova ou textos sem link. O filtro não foi calibrado pelo benchmark completo e não deve ser apresentado como solução geral de precisão.

## Evidências atuais

- `testes-ui.txt`: 18 testes aprovados, seis novos em `tests/ui/test_conversation.py`.
- `testes-ia.txt`: 27 testes correntes aprovados (incluem sete da correção documental anterior).
- `testes-v2.txt`: 21 métodos históricos aprovados, sem edição da suíte V2.
- `integracao.json`: cliente real → NestJS → FastAPI → ChromaDB. Continuação retornou ausência de endereço e fontes de regras/PPC IA. Ainda recuperou trecho de TG: limitação observada.
- `apptest.json`: execução do app com AppTest oficial e HTTP simulado. Verificou continuação sem exceção e histórico limpo ao mudar curso. Não é inspeção visual em navegador nem teste da rede real.
- `../20261110-texto-pdf/`: reingestão 21/21, correção da extração vertical e 6.779 trechos no Chroma local. Base local não acompanha Git/ZIP; reproduzir com ingestão.

Não foi reexecutada a regressão do backend, pois não há alteração nesse componente. Os 256 testes e o benchmark 25/50 citados nos relatórios são resultados anteriores. Suítes V1/V2, snapshots, hashes históricos e PDFs antigos ficam preservados. Os novos ajustes são funcionais, não contam como refatorações acadêmicas adicionais. As três refatorações principais continuam comprovadas nas revisões correspondentes.

## Reproduzir

Na raiz, com o venv: `python -m unittest discover -s tests/ui -v`.
Em ai-service: `python -m unittest discover -s tests -v` e `python -m unittest discover -s tests/v2 -v`.
Com serviços parados, outro computador precisa executar `python -m src.ingest_batch` em ai-service após instalar dependências. Iniciar os três serviços conforme README, limpar o histórico e perguntar sobre segunda chamada seguido de “Onde consigo esse requerimento?”. O endereço não está no trecho atual de regras; não foi inventado nem pesquisado um novo endereço oficial.

PDFs para esta revisão: `docs/testes/analise-critica-sprint3-conversa-20261110.pdf` (5 páginas) e `docs/qualidade/relatorio-refatoracoes-sprint3-conversa-20261110.pdf` (3 páginas). Conferir links e fazer commit/push/merge antes do Classroom. Não considerar a simples existência deste pacote como revisão humana ou aceite da professora.
