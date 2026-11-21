# Chatbot SecGrad — Assistente de Orientação Acadêmica

Frontend React 18/Vite/Cinnamon e backend NestJS 11/Node 24 adaptados dos dois boilerplates CInCoders fornecidos à equipe. O serviço Python FastAPI/ChromaDB mantém a recuperação documental.

**Estado real:** código migrado e validado por testes e builds locais. O conjunto Docker/PostgreSQL/Keycloak ainda precisa ser executado em máquina com Docker. O realm incluído é de desenvolvimento; LDAP institucional depende da configuração do CIn. A geração pode usar a API da OpenAI quando configurada. A integração tem testes locais com respostas simuladas do provedor e aguarda validação com uma conta autorizada.

## Arquitetura

```text
React + Cinnamon → Keycloak (login)
       │ Bearer token
       ▼
NestJS /secgrad/api/v1/conversa → FastAPI → ChromaDB + documentos
       │
       └→ PostgreSQL/Prisma (base do template e verificação de saúde)
```

As perguntas não são persistidas no PostgreSQL nesta versão. A conversa fica no estado da tela e é descartada ao limpar, mudar curso/perfil ou recarregar. O PostgreSQL mantém a infraestrutura Prisma do template; as tabelas de tarefas do exemplo não estão expostas como funcionalidade do chatbot.

## Executar no Windows — forma recomendada

Pré-requisitos: Git, Docker Desktop com engine Linux/Compose V2 ativo; Node.js 24 para testes e desenvolvimento fora dos contêineres. O ambiente Python local existente pode continuar sendo usado para os testes de IA.

Na raiz do repositório, no PowerShell:

```powershell
Copy-Item .env.example .env
docker compose up -d --build ai-service
docker compose exec ai-service python -m src.validate_catalog
docker compose exec ai-service python -m src.ingest_batch
docker compose up -d --build
docker compose ps
```

Só copie o exemplo se ainda não existir `.env`. Não sobrescreva configurações pessoais/institucionais. A primeira ingestão pode baixar o modelo de embeddings e demorar. O banco vetorial local antigo não é automaticamente copiado para o volume Docker: a ingestão acima cria a base do contêiner com o catálogo atual.

Abra **http://localhost:5173/secgrad/**. Use `user` / `user` para o usuário de desenvolvimento ou `admin` / `admin` para o administrador do realm local. Essas contas são fornecidas pelo template e **não são contas LDAP**. A senha administrativa do console do Keycloak vem de `KEYCLOAK_ADMIN_PASSWORD` no `.env` (console em http://localhost:8080/auth).

Um comando auxiliar equivalente é `./scripts/iniciar-templates.ps1`; ele verifica se Docker está disponível e só ingere documentos quando solicitado com `-Ingerir`.

Para parar: `docker compose down`. Esse comando preserva volumes. Não use `down -v` se quiser manter bancos e índices.

## Desenvolvimento com terminais separados

Primeiro, configure `.env` na raiz e inicie os bancos/Keycloak:

```powershell
docker compose up -d postgres keycloak
```

Terminal 1, raiz do projeto, usando o Python já instalado:

```powershell
.\venv\Scripts\Activate.ps1
cd ai-service
$env:SECGRAD_GENERATION_MODE = "mock"
python -m uvicorn main:app --port 8000 --host 127.0.0.1
```

Em uma instalação nova, crie um ambiente Python e instale `ai-service/requirements.txt`. Caso a base local ainda não exista, execute `python -m src.ingest_batch` dentro de `ai-service` antes de iniciar o serviço.

Terminal 2:

```powershell
cd backend
Copy-Item .env.example .env
npm.cmd ci
npm.cmd run prisma:generate
npm.cmd run migration:run
npm.cmd run build
npm.cmd start
```

Terminal 3:

```powershell
cd frontend
Copy-Item .env.example .env
npm.cmd ci
npm.cmd run dev
```

As credenciais e URLs dos ambientes devem coincidir. O `.env.example` do backend usa a mesma configuração local padrão do Compose. Se alterar senha/realm/cliente no `.env` da raiz, ajuste também os arquivos dos serviços. Depois de editar TypeScript do backend, reexecute o build antes de iniciar; não use o antigo comando Streamlit como interface oficial.

## Testes

```powershell
cd backend
npm.cmd ci
npm.cmd run prisma:generate
npm.cmd test
npm.cmd run test:e2e
npm.cmd run lint
npm.cmd run build
cd ..\frontend
npm.cmd ci
npm.cmd test
npm.cmd run lint
npm.cmd run build
cd ..\ai-service
..\venv\Scripts\python.exe -m unittest discover -s tests -v
```

Os testes HTTP de migração usam o bootstrap real, substituindo PostgreSQL e o provedor externo por dependências de teste. A validação de JWT tem teste separado com assinatura RSA e servidor JWKS locais reais. Isso **não substitui** executar o login no Keycloak e a integração institucional.

As regressões do contrato HTTP anterior ficam identificadas em `backend/test/legacy-support`; não são rotas públicas da aplicação nova. Os testes históricos `backend/test/sprint3-v2` e os relatórios da Sprint 3 foram preservados; são evidências das revisões anteriores, não medições automáticas da migração.

## Geração por LLM

Para usar a API da OpenAI no Compose, configure `SECGRAD_GENERATION_MODE=openai` e `OPENAI_API_KEY` no `.env` local. `SECGRAD_OPENAI_MODEL` é opcional e usa `gpt-5.4-mini` por padrão. Com FastAPI executado diretamente, defina essas variáveis no ambiente do processo. Use uma chave de projeto autorizada, armazenada somente no servidor, e perguntas de teste sem dados pessoais. O modo `mock` continua disponível para testar a integração local.

O serviço envia à API a pergunta e os trechos recuperados. O modelo retorna texto e citações literais. Uma resposta sem evidência identificável devolve `null`, que aciona o fallback existente no Nest. Uma falha do provedor devolve `503`. A conferência literal verifica a presença dos trechos e dos links citados. A correção da orientação precisa ser avaliada com perguntas de referência.

Antes da demonstração, reingira o catálogo para incorporar o endereço oficial de segunda chamada e ensaie uma consulta com fonte, uma pergunta fora do escopo e um caso de indisponibilidade do provedor.

## Contrato e comportamento

- Rota autenticada: `POST /secgrad/api/v1/conversa`.
- Sucesso: envelope do template com `statusCode`, `timestamp`, `path`, `data`.
- Erros: Problem Details; 401/403 para identidade/permissão, 422 para entrada inválida, 502/503/504 para falhas técnicas externas.
- Campos do chatbot ficam em `data`: `resposta`, `fontes`, `contexto`, `distancia_minima`, `fallback_acionado` e, quando necessário, `template_email`/`setor_sugerido`.
- Cada fonte inclui arquivo, página, curso e trecho associado. Formatos não reconhecidos não recebem citação inventada.
- `historico` opcional recebe até dez perguntas anteriores; resolve apenas referências limitadas a requerimentos de segunda chamada, não uma memória conversacional geral.
- Limiar `0.8` permanece provisório; distância vetorial não é probabilidade de acerto.
- Simulação não responde fatos acadêmicos. Trechos recuperados podem ser irrelevantes; ausência de link não autoriza inventar endereço.
- `/api/v1/ingestar` existe somente no serviço interno de IA; não há proxy público de ingestão no NestJS.

Exemplo de corpo (com Bearer válido no cabeçalho):

```json
{"consulta":{"pergunta":"Como solicito segunda chamada?","curso":"IA","perfil":"novo","top_k":3},"historico":[]}
```

## Limites e implantação institucional

O Compose usa as versões locais de Keycloak/PostgreSQL da base fornecida, sem certificar que sejam as versões aprovadas para produção. Antes de publicar, alinhe versão do Keycloak, LDAP, clientes/papéis, HTTPS, senhas e URLs com os responsáveis. Variáveis `VITE_*` são públicas; nunca inclua segredo de cliente nelas.

Não remova os guards para contornar um erro de login. O backend exige configuração do Keycloak e não oferece desativação silenciosa da autenticação.

## Documentação e origem

- [Guia da migração e pendências](docs/MIGRACAO-TEMPLATES.md).
- [Contrato autenticado](docs/contrato-api-template.md).
- [Origem e identificação dos templates](template-sources.json).
- [Índice histórico da Sprint 3](docs/ENTREGA-SPRINT3.md).

Os arquivos Python de interface na raiz e em `src/ui` são o protótipo histórico Streamlit. Não fazem parte do caminho oficial React → NestJS e não foram usados como prova de aderência ao template.
