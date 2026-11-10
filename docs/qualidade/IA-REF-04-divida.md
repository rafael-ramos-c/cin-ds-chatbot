# IA-REF-04 - Separar leitura da fonte e montagem do contexto

Local: ai-service/src/retriever.py, buscar_contexto, bloco nome_documento /
numero_pagina / curso_documento e validação de página no laço de resultados.

Diagnóstico por inspeção assistida: a função mistura acesso à coleção, política
de aliases dos metadados, validação de página e construção das apresentações.
Long Method / coesão / orientação SRP no nível da função. A política de aliases
é uma responsabilidade distinta: mudar chaves legadas hoje exige navegar pela
montagem de contexto e fontes. Não se afirma violação de todos os princípios
SOLID nem que a extração elimine o acoplamento ao ChromaDB.

Escolha: Extract Function, extrair literalmente as leituras e a rejeição de página
inválida para _ler_fonte(metadata), com retorno nome/página/curso. Preservar ordem
dos .get (inclusive avaliação eager dos defaults), precedência de chaves, valores
padrão, tipos e mensagens. Manter chamadas antes de construir cabeçalho/contexto.
Não mudar filtros, distâncias, payload ou política de fallback.

Proteção principal: V2 acadêmica US-01 preservada em ai-service/tests/v2/,
incluindo V1 importada por ela. Antes: 21 métodos aprovados; coverage.py 7.17.0,
branches ligados, escopo src.retriever + src.metadata_utils. Mesmo comando e
escopo depois; hashes dos testes devem coincidir. Evidências em IA-REF-04-evidencias.

Esta é execução nova e adicional, não reconstrução de 30/10 nem substituição da
comparação V1/V2 histórica. BACK-REF-03 permanece como evidência complementar,
protegida pela regressão corrente. IA-REF-04 permite ter três itens diretamente
protegidos pelas V2 acadêmicas: BACK-REF-01, IA-REF-02 e IA-REF-04.

Status inicial: identificado e medido antes; aplicar somente após salvar o estado.
Rafael assumiu o fechamento com assistência neste chat; revisão humana do grupo
não é substituída por assinatura inventada.
