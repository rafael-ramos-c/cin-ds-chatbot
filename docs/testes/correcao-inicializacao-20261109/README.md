# Correcao do roteiro de inicializacao — 09/11/2026

## Diagnostico
O print da interface apresenta HTTP 503 com `Servico de busca nao configurado`.
A excecao corresponde a AI_SERVICE_URL ausente/invalida no processo NestJS.
O README do backend continha uma primeira inicializacao sem essa variavel.
Nao foi necessario remover a validacao de URL nem alterar o contrato HTTP.

## Alteracoes
- backend/scripts/iniciar-local.ps1: configura a origem local e timeout de desenvolvimento somente quando ausentes, valida-os e inicia npm.cmd run start:dev no diretorio correto.
- README.md: roteiro PowerShell completo dos tres terminais; distingue simulacao de integracao de resposta academica real.
- backend/README.md: corrige o primeiro comando Bash e aponta para o roteiro Windows.

## Verificacao
- Defaults de URL/timeout e preservacao de valores existentes: aprovados.
- Quatro URLs invalidas e cinco timeouts invalidos: rejeitados.
- Invocacao do npm com argumentos, diretorio, ambiente e retorno ao diretorio original: verificada com comando substituto controlado, sem iniciar watch nessa verificacao.
- integracao-real.json: dez cenarios HTTP com FastAPI, corpus e NestJS reais aprovados; sem configuracao reproduz o mesmo 503 do print e com configuracao retorna conversa 201.
- live-opt-in.json: dois testes de integracao aprovados.
- git diff --check sem problemas.

Os processos temporarios do ensaio foram encerrados. As suites historicas,
interface, regras de URL, limiar de fallback e PDFs nao foram alterados.
A geracao foi explicitamente simulada: este ensaio nao substitui benchmark de
respostas, LLM real ou validacao no navegador. Nao conta como refatoracao formal.
O OCR pendente dos documentos nao foi executado nesta correcao.

## Uso pelo Eric
Apos atualizar o repositorio, seguir o roteiro PowerShell na raiz do README.
Reiniciar o NestJS pelo script (variaveis so afetam processos iniciados depois).
Iniciar tambem o FastAPI no terminal proprio. O script do backend nao inicia a IA.
