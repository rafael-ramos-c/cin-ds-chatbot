# IA-REF-04 - Evidência direta da V2 acadêmica

Esta refatoração reforça a aderência ao roteiro: os três itens principais passam
a ser BACK-REF-01, IA-REF-02 e IA-REF-04, protegidos diretamente pelas V2 da Parte 1.
BACK-REF-03 permanece válido como complemento, sem reatribuir sua regressão corrente
à V2 acadêmica antiga. Não se apaga a entrega anterior nem se inventa execução antiga.

Local: ai-service/src/retriever.py, buscar_contexto. Extract Function para
_ler_fonte(metadata): precedência documento/source, pagina/page e curso_alvo/curso,
valores padrão e validação exata de página ficam juntos. O laço recebe a tupla
antes de formatar cabeçalho e acrescentar contexto/fontes. Mesmas operações,
mesma ordem dos get, mesmos defaults eager e mesma exceção. Nenhum contrato mudou.

O código antes e depois está nos snapshots de IA-REF-04-evidencias. O diagnóstico
foi registrado antes do código em IA-REF-04-divida.md. A escolha é de baixo risco
porque o trecho está coberto por casos de fonte, múltiplas fontes e página inválida.
Não se afirma remover todas as responsabilidades do retriever ou melhorar a busca.

Congelamento: c93450a; HTML anterior: c9328fe; alteração isolada: c0f7116.
V2 acadêmica: mesmos 21 métodos aprovados antes e depois; hashes dos testes V2 e
V1 importada conferidos iguais. Coverage.py 7.17.0, branches ligados, mesmo comando
e escopo src.retriever + src.metadata_utils. Execução, JSON e HTML acompanham ambas.
Linhas: 93/97 (95,88%) -> 96/100 (96%); branches: 41/42 (97,62%) em ambos. A função
adiciona definição, retorno e chamada instrumentados: percentual de linhas aumenta
sem acrescentar casos de teste. Quatro linhas e um branch continuam descobertos.

As 20 regressões da IA e dez cenários HTTP com dois testes opt-in também passaram
após a mudança. A integração é real, mas a geração continua mock; não confundir
com precisão semântica ou reprodução de benchmark posterior. O benchmark de 25
casos foi preservado, não reexecutado nesta rodada, pois a mudança não altera
consulta, ranking, embeddings ou corpus.

Reprodução em ai-service: python scripts/medir_us01.py v2 DESTINO_NOVO.
Esse comando já existia; não foram mudados seu escopo nem o código dos testes.
Use pasta nova para não sobrescrever registros. Documento preparado com apoio
neste chat; revisão humana do diagnóstico continua necessária.
