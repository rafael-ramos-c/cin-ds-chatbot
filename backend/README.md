# Backend SecGrad — base NestJS CInCoders

Node.js 24, NestJS 11, ConfigModule, Prisma/PostgreSQL, Zod, Keycloak/JWKS, papéis, Swagger e contrato envelopado do template.

O guia de execução está no [README da raiz](../README.md). A configuração de referência é `.env.example`; autenticação é obrigatória. A rota de conversa é `POST /secgrad/api/v1/conversa`. O healthcheck público fica em `/secgrad/api/health` e verifica o PostgreSQL.

## Módulos

- `src/common/auth`: validação de identidade e papéis do template.
- `src/database`: infraestrutura Prisma.
- `src/modules/health`: saúde da aplicação/banco.
- `src/modules/conversation`: controller, DTO, continuidade limitada e associação de trechos.
- `src/orchestration`: regras do SecGrad, limiar e fallback.
- `src/ai-service`: comunicação segura com FastAPI, timeout e validação do retorno.
- `src/configure-app.ts`: prefixo, versão, CORS, filtro e interceptador compartilhados com os testes HTTP.

`npm run build` resolve também os aliases TypeScript, para o JavaScript compilado executar diretamente com Node. `npm start` executa esse build. Após alterar fontes, recompile.

`npm test` executa regressões do domínio, regressões explicitamente isoladas do contrato antigo e testes da migração. `npm run test:e2e` executa o contrato HTTP autenticado com dependências externas substituídas para teste. `npm run test:cov` gera relatório de cobertura da revisão atual. Não confunda essas métricas com a V1/V2 histórica da Sprint 3.

A fixture em `test/legacy-support` reproduz o contrato antigo apenas para regressões. Não é importada pelo AppModule de produção. `test/sprint3-v2` conserva o conteúdo histórico e fica fora da suíte corrente.

Os scripts antigos de evidências em `scripts/` pertencem à entrega anterior; para validar o contrato novo use os comandos e o guia acima. Não basta trocar a URL desses scripts: agora há token e envelope `data`.
