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
