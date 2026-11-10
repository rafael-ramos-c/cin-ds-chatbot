# Log de Análise e Evidências — Processamento de OCR dos PPCs

## 1. Contexto e Identificação do Problema
Durante a preparação dos dados para o sistema RAG, identificou-se que os ficheiros PDF institucionais (PPCs) continham páginas escaneadas em formato de imagem pura, sem camada de texto pesquisável, o que impedia a extração correta pelo pipeline de ingestão.

## 2. Páginas Alvo Analisadas e Processadas
- **`ppc_ec_anterior.pdf`**: Página física **22**[cite: 4].
- **`ppc_si_anterior.pdf`**: Página física **202**[cite: 4].
- **`ppc_si_novo_2024.pdf`**: Páginas físicas **149, 158 e 159**[cite: 4].

## 3. Análise, Execução e Validação
- **Ferramentas utilizadas**: Motor Tesseract-OCR e ferramenta `ocrmypdf` operando em ambiente virtual configurado no VS Code.
- **Verificação de Resultados**: 
  - Os PDFs foram atualizados no caminho canónico (`data/raw/`), mantendo os nomes e a estrutura original intactos[cite: 4].
  - Validação manual efetuada no leitor de PDF local: confirmou-se que o texto das páginas indicadas tornou-se totalmente selecionável e copiável, preservando integralmente o conteúdo visual e a quantidade original de páginas[cite: 4].
- **Decisão**: Documentação de governança consolidada em `docs/qualidade/` para auditoria do processo antes da reingestão final no ChromaDB.