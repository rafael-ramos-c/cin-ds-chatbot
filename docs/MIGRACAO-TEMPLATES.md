# Migração para os templates CInCoders — 12/11/2026

Este documento registra a execução original da migração. Para o escopo e a execução atuais com Docker, Qwen e autenticação local, consulte o [fechamento da Sprint 4](ENTREGA-SPRINT4.md).

## O que mudou

O frontend oficial agora fica em `frontend/`, baseado no boilerplate React/Vite/Cinnamon recebido. O backend foi adaptado ao boilerplate NestJS com ConfigModule, Prisma, autenticação Keycloak/JWKS, RBAC, envelope de sucesso, Problem Details e health check. O domínio de busca, geração e fallback foi integrado a essa estrutura. O serviço FastAPI e o catálogo documental foram preservados.

A rota oficial passa a ser `POST /secgrad/api/v1/conversa`, autenticada, com os dados dentro de `data`. O frontend já usa esse contrato. Fontes têm trechos associados por arquivo/página/curso; texto é exibido como texto, sem executar HTML fornecido nos documentos. Mudança de curso/perfil limpa a conversa. Referências a requerimentos de segunda chamada recebem tratamento limitado e explícito; não há memória conversacional geral.

O protótipo Streamlit em `app.py` e `src/ui` permanece histórico. Nenhum módulo de chat persiste perguntas no PostgreSQL. As tabelas de tarefas do template permanecem como infraestrutura de exemplo, sem API pública de tarefas. A geração `mock` continua claramente identificada e não constitui orientação acadêmica produzida por LLM.

## Origem e preservação

`template-sources.json` identifica os diretórios recebidos, suas impressões digitais e a revisão anterior do projeto. Os scripts de geração POSIX não foram executados: os nomes foram substituídos em uma cópia local, respeitando a estrutura dos templates.

Antes das mudanças, foi criado backup completo externo, incluindo Git, ambientes e ChromaDB: `cin-ds-chatbot-completo-antes-templates-20261112-141919.zip`. SHA-256: `4a792087e8ddb6f02d0fb3882a597e817a73b0cfae85b1a6a5b49f61f0e4022d`. O arquivo e seu manifesto ficam na pasta `backups` do trabalho Codex; não devem ser publicados pois contêm configurações e ambientes locais.

Os PDFs, matriz, logs e suítes históricas da Sprint 3 não foram recalculados ou reescritos para aparentar resultados da migração. Testes HTTP do contrato antigo utilizam um módulo explícito em `backend/test/legacy-support`; esse contrato não é exposto em produção. A execução histórica exige sua revisão/configuração original.

## Validação realizada e limites

Os resultados finais dos comandos locais estão em `docs/migracao/evidencias/resumo.json` e logs adjacentes. Foram verificados testes, lint e build de backend/frontend e regressões unitárias Python. Também abriu a tela de login React no navegador.

Um teste adicional fez a chamada com JWT assinado e JWKS local, usando o NestJS e o FastAPI/ChromaDB reais. Apenas o banco relacional foi substituído nesse teste. Isso verifica o caminho documental autenticado, mas não comprova conexão com o Keycloak institucional, LDAP ou PostgreSQL real.

Docker não está instalado nesta máquina: as imagens, Compose, migrações PostgreSQL e login completo com o realm local ainda NÃO foram executados. O YAML foi revisado estruturalmente; não tratar isso como validação operacional do Compose. As versões de infraestrutura reproduzem as bases fornecidas e precisam de aprovação/atualização antes de produção.

## Como continuar

1. Siga o README da raiz em máquina com Docker Desktop/Compose ativo. Configure `.env`, inicie IA, ingira o catálogo e suba o conjunto. Abra `http://localhost:5173/secgrad/`.
2. Valide login/logout de `user` e `admin`, token expirado, acesso sem token, pergunta com fontes, fora de escopo, timeout e indisponibilidade da IA.
3. Alinhe com o CIn os endereços, realm, clientes, papéis e federação LDAP. Não é possível configurar a federação institucional sem essas informações e o acesso administrativo correspondente. Não remova autenticação para contornar configuração.
4. Se a próxima entrega exigir resposta por LLM real, escolha e configure o provedor, mantendo evidências, limites e falhas técnicas. Esta migração não conecta serviço pago nem finge geração real.
5. Refaça o benchmark na nova revisão antes de declarar equivalência funcional completa. Os relatórios anteriores documentam a Sprint 3 histórica.

Para repetir o teste documental opcional: inicie o FastAPI local com a base ingerida, entre em `backend`, defina `$env:SECGRAD_LIVE_TEST='1'` e `$env:AI_SERVICE_URL='http://127.0.0.1:8000'`, e execute `npm.cmd run test:live`. O teste usa identidade de laboratório, não credenciais institucionais.

## Retorno ao estado anterior

O backup é completo. Para inspecionar/restaurar, extraia-o em OUTRA pasta primeiro e confira o conteúdo e o manifesto. Não sobrescreva uma pasta com novos trabalhos de colegas. Nenhum push, merge ou commit foi realizado automaticamente nesta adaptação.


## Resultados finais desta revisão

- Backend: 293 testes aprovados; suíte HTTP da migração: 25 casos aprovados (também contidos nos 293); lint sem erros; build aprovado.
- Frontend: 49 testes aprovados; lint e build aprovados.
- IA: 27 testes unitários aprovados; código de recuperação preservado.
- Integração documental opcional: 1 teste aprovado com FastAPI/Chroma reais e identidade de laboratório.
- 551 arquivos preexistentes protegidos conferidos por SHA-256, sem alterações, incluindo catálogo, IA e materiais históricos.
- Cobertura backend: linhas 93,33%, branches 85,71%, no recorte configurado. Frontend: linhas 95,68%, branches 84,48%, apenas chat e cliente HTTP. Esses números não significam cobertura integral de infraestrutura ou autenticação externa.
- `npm audit --omit=dev`: nenhum alerta nas dependências de execução nas duas aplicações, no momento desta verificação. Ainda há alertas em ferramentas de desenvolvimento (5 no backend, 7 no frontend), documentados como pendência; não foi forçada mudança para NestJS 12.
- O lint do backend conserva 24 avisos de estilo em testes, sem erros. O build frontend avisa sobre o tamanho do pacote principal; otimização por divisão de pacotes fica para evolução.

As dependências foram atualizadas de forma compatível quando possível, inclusive Vitest e Zod. O pequeno CSS do shadcn foi preservado localmente com licença MIT em `frontend/src/styles`, dispensando o gerador CLI inteiro como dependência de build. Nenhuma conversa pessoal foi transcrita nos arquivos desta migração.
