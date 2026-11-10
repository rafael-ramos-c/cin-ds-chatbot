# Registo de Dívida Técnica — Qualidade e OCR dos PPCs

Este documento consolida as dívidas técnicas e o estado da qualidade associados ao processamento de OCR e à governação documental na Sprint 3.

| ID | Dívida técnica | Impacto | Prioridade | Responsável | Status | Plano de pagamento | Critério de conclusão |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DATA-02 | PPCs dos quatro cursos ainda não foram incorporados ao catálogo final | A base não cobre integralmente informações curriculares | Alta | Ricardo e Rafael | **Resolvido** | Ricardo adiciona documentos e metadados; Rafael valida e reingere | Validador passa, todos os PPCs com OCR são ingeridos e consultas por curso retornam fontes corretas[cite: 4] |
| DATA-01 | Existem documentos duplicados em `data/raw` e `ai-service/data` | Risco de ingerir versões diferentes, incluindo PDFs sem OCR | Alta | Rafael e Ricardo | **Resolvido** | Confirmar `data/raw` como fonte canônica com os PDFs corrigidos via OCR e remover cópias antigas | Existe somente uma origem documental validada, com camada OCR pesquisável e documentada |