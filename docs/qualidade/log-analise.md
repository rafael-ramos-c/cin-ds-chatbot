# Log de Análise e Evidências — Processamento de OCR dos PPCs

## 1. Contexto e Identificação do Problema
Durante a preparação dos dados para o sistema RAG, identificou-se que os ficheiros PDF institucionais (PPCs) continham páginas escaneadas em formato de imagem pura, sem camada de texto pesquisável, o que impedia a extração correta pelo pipeline de ingestão.

## 2. Páginas Alvo Analisadas e Processadas
- **`ppc_ec_anterior.pdf`**: Página física **22**.
- **`ppc_si_anterior.pdf`**: Página física **202**.
- **`ppc_si_novo_2024.pdf`**: Páginas físicas **149, 158 e 159**.

## 3. Análise, Execução e Validação
- **Ferramentas utilizadas**: Motor Tesseract-OCR e ferramenta `ocrmypdf` operando em ambiente virtual configurado no VS Code.
- **Verificação de Resultados**: 
  - Os PDFs foram atualizados no caminho canónico (`data/raw/`), mantendo os nomes e a estrutura original intactos.
  - Validação manual efetuada no leitor de PDF local: Ricardo relatou texto selecionável e conteúdo visual preservado. A verificação independente de 09/11 confirmou texto extraível em quatro páginas, mas não em EC, página 22; a quantidade de páginas dos três PDFs permaneceu igual. A fidelidade visual/semântica do OCR não é certificada apenas por extração.
- **Decisão**: Documentação de governança consolidada em `docs/qualidade/` para auditoria do processo antes da reingestão final no ChromaDB.

## 4. Verificação independente de Rafael em 09/11/2026

PR #35 integrado na revisão b40c4f43f055d704462efa02074d7413a0e0092d.
Comparação por pypdf contra a revisão anterior 69b2587, sem executar novamente
OCR nem sobrescrever PDFs. Resultado e hashes em
[comparação OCR](../testes/validacao-pos-ocr-20261109/ocr-comparacao.json).
SI anterior 202 e SI novo 149/158/159 passaram a fornecer texto. EC anterior 22
continua sem texto extraível; não classificar todas as páginas como corrigidas.

A inspeção também confirmou cópias em ai-service/data/. A ingestão usa data/raw/
via src/config.py, mas a remoção ou o arquivamento do legado ainda não ocorreu.
Os dois itens foram separados no registro de dívidas, evitando status de resolução
sem evidência. Não foram removidos arquivos de Ricardo nem alterada a interface.

Método: leitura dos arquivos e histórico Git, comparação automatizada de extração,
reingestão e auditoria do ChromaDB; apoio de LLM/Codex neste chat. Não há registro
separado que permita atribuir cada descoberta exclusivamente à pessoa ou à LLM,
nem execução de ferramenta de diagnóstico de smells. Evidências da rodada:
[índice de validação](../testes/validacao-pos-ocr-20261109/README.md).


## 5. Fechamento assumido de Eric e Victor - 10/11/2026

Pedido de Rafael neste chat: "Os dois me mandaram um mensagem, e o Eric também
me mandou um print. Baseado em tudo isso, tente finalizar/ajustar esse final da
Sprint 3 para eu poder entregar à professora." Rafael informou que assumiu o
fechamento de Eric, além do de Victor.

Contexto recebido: Eric relatou correção local do padrão para 0,8, 256 testes
no Node 22 e ausência de benchmark preenchido/terceira refatoração no ZIP.
Nada disso foi atribuído a execução no GitHub: main continuava cd583e4 com 0,5.
Ricardo informou verificação de EC22 como contracapa escura e legibilidade do
OCR de SI. Sua mensagem, não um novo commit, é a origem dessa validação local.

Verificação independente: EC22 foi renderizada e inspecionada; é página escura
com etiqueta de processo/implantação do curso, sem texto curricular corrido.
Imagem e hash do PDF no fechamento. Justifica exclusão da recuperação curricular,
sem apagar página, renumerar fontes ou declarar OCR concluído nessa página.

Módulo examinado para BACK-REF-03: AiService, especificamente getEndpoint.
O predicado de sete verificações foi extraído para origemInvalida, sem mudar a
ordem OR, regex, rota ou catch. Diagnóstico, escolha, falsos enquadramentos e
execuções em BACK-REF-03-divida.md e BACK-REF-03-evidencias/.

Ferramentas/configuração: Node 24.22.1, Vitest/coverage-v8 instalados, cobertura
restrita ao AiService, Oxlint type-aware e Nest build. A mesma suíte corrente
V2 de regressão teve 256/256 antes/depois e hashes conferidos; não confundir
com os 105 testes acadêmicos históricos. Função adicional explica denominador
64->65 linhas e 10->11 funções; branches permanecem 84/84.

Apoio: Codex/LLM neste mesmo chat; snapshot de implantação não disponibilizado.
Não houve ferramenta de smells nem comparação experimental separada de autoria
humana versus LLM. A inspeção de diff e os testes confirmam preservação dentro
do alcance medido; leitura final pelos colegas continua recomendada.

O benchmark utilizou 25 entradas predefinidas, corpus real e geração mock. A
primeira medição usava nomes esperados PPC com capitalização incorreta; o oráculo
foi corrigido para arquivos reais e o ensaio repetido, preservando a primeira
execução. Não se alteraram perguntas para produzir resultados favoráveis nem
se classificaram falhas como sucesso. Limiares 0,8/0,5 não foram calibrados.

Fontes públicas para o AppTest headless utilizado:
https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest
O teste usa HTTP real aos processos temporários, sem navegador, e não substitui
inspeção visual humana. PDFs finais foram renderizados e conferidos página a página.
