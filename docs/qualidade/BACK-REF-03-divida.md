# BACK-REF-03 - Separar política de origem da construção do endpoint

Local: backend/src/ai-service/ai-service.service.ts, getEndpoint.

Diagnóstico: o método combina leitura de configuração, parsing URL, predicado
com sete verificações de origem, construção da rota e tradução de exceções.
O predicado ocupa o centro do fluxo e dificulta reconhecer a responsabilidade
específica da política de origem. Categoria: Long Method relativo ao fluxo,
coesão de método e separação de responsabilidades (SRP como orientação local,
não alegação de que toda a classe viola todos os princípios SOLID).

Consequência: revisar a política exige navegar por construção de rota e tratamento
HTTP. Um nome de função explicita onde a política começa e termina.

Escolha: Extract Function para origemInvalida(origin, base), interna ao módulo,
com as mesmas condições OR na mesma ordem, mesmos valores truthy/falsy e regex.
getEndpoint mantém o try/catch, leitura de ambiente, new URL e rota. Não mudar
defaults, exceções, timeout, filtros, payload, nem converter em nova funcionalidade.

Proteção: executar antes/depois a mesma suíte corrente V2 de regressão (256 casos),
que contém as regressões de URL e os 52 casos de geração citados por Eric.
Configuração congelada: backend/vitest.back-ref03.config.mts; cobertura restrita
ao AiService. Os testes acadêmicos V1/V2 históricos permanecem imutáveis e não
são reatribuídos a esta nova execução. Status: Refatorado. Execução anterior congelada em 2a33101; alteração isolada em 27d0d9b. Antes/depois 256/256, mesma suíte e configuração. Linhas: 64/64 e 65/65; branches: 84/84 em ambos. Evidências e hashes nas pastas antes/depois.

Identificação: inspeção do módulo com apoio de Codex/LLM neste chat em 10/11.
Rafael assumiu esta etapa de Eric; autoria da execução não é atribuída a Eric.
