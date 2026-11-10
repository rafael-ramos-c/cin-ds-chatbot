# BACK-REF-03 - Extract Function, 10/11/2026

Rafael assumiu o fechamento de Eric. Não é uma refatoração atribuída retroativamente
a Eric nem o tratamento de timeout que já existia no código.

Local: AiService.getEndpoint, backend/src/ai-service/ai-service.service.ts.
Antes, parsing, sete condições de validade, rota e tradução de erros se misturavam.
Depois, origemInvalida(origin, base) contém literalmente as sete condições OR,
na mesma ordem. getEndpoint continua responsável por leitura, parsing, rota e catch.
A função é interna; não há contrato novo, exportação, alteração de mensagens,
remoção de segurança ou mudança do timeout. A classificação de baixa coesão e
Long Method se refere ao fluxo do método, não à quantidade absoluta de linhas
nem à alegação de resolver SRP de toda a classe.

Escolha: mudança pequena no trecho de origem que já tem testes de fronteiras,
origens inválidas e rotas de busca/geração. Função nomeada explicita a política.

Commits: correções funcionais em 0b334a7; suíte anterior congelada em 2a33101;
refatoração isolada em 27d0d9b. Links permanentes após publicar a branch:
https://github.com/rafael-ramos-c/cin-ds-chatbot/commit/27d0d9b

Mesma suíte V2 de regressão corrente antes/depois: 256/256 no Node 24.22.1.
Inclui os 52 testes de geração, mas eles não são somados novamente ao total.
A V2 acadêmica histórica de 105 casos não foi reexecutada nem alterada para fingir
compatibilidade com geração adicionada posteriormente. Há duas camadas de evidência:
histórico acadêmico preservado e proteção atual da refatoração, explicitamente
identificadas. Isso limita a equivalência estrita com a baseline antiga da Parte 1.

Cobertura do mesmo arquivo: linhas 64/64 -> 65/65 (100%); branches 84/84 -> 84/84
(100%). A nova função aumenta denominadores de funções/linhas, não comportamento.
Funções 8/10 -> 9/11: não dizer 100% de todas as métricas. Ver comparacao.json.

Configuração: backend/vitest.back-ref03.config.mts, BACK_REF03_EVIDENCE_DIR com
destino antes/depois. Comando em backend: node node_modules/vitest/vitest.mjs run
--config vitest.back-ref03.config.mts --coverage. Hashes UTF-8/LF da suíte foram
conferidos, para não confundir conversão CRLF do Windows com mudança de teste.

Antes/depois e HTML em BACK-REF-03-evidencias/. Lint e build correntes aprovados;
dois avisos no-base-to-string preexistentes em testes não foram removidos à força.
Resultado não certifica precisão semântica do RAG ou LLM real.
