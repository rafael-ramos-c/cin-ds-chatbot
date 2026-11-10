# Benchmark observacional - Sprint 3, 10/11/2026

25 perguntas definidas antes da medição: dez legadas, sete controles de PPC e oito negativas adicionais. Fontes/páginas/contextos e minutas integrais estão em benchmark-entrega/benchmark.json. Foram feitas 50 chamadas de conversa comparativas, além de aquecimento e duas interações da UI. Geração mock, sem avaliar resposta acadêmica de LLM.

| Caso | Pergunta | Curso/perfil | Fallback esperado | Distância | Fallback 0,8 | Fallback 0,5 |
| --- | --- | --- | --- | --- | --- | --- |
| LEG-01 | Como solicito dispensa de disciplina cursada externamente? | CC/novo | Não | 0.409167 | Não | Não |
| LEG-02 | Qual o prazo para pedir segunda chamada de prova? | CC/novo | Não | 0.399827 | Não | Não |
| LEG-03 | O estágio não obrigatório pode ser iniciado antes da assinatura do termo? | CC/novo | Não | 0.295805 | Não | Não |
| LEG-04 | Aluno de Ciência da Computação pode pagar estágio em empresa sem convênio com a UFPE? | CC/novo | Não | 0.327346 | Não | Não |
| LEG-05 | Quais são os requisitos para trancamento total de semestre? | CC/novo | Não | 0.418048 | Não | Não |
| LEG-06 | Onde encontro o formulário de equivalência de componentes curriculares? | CC/novo | Não | 0.212840 | Não | Não |
| LEG-07 | Quem é o responsável por assinar o termo de compromisso de estágio de Engenharia da Computação? | EC/novo | Não | 0.256873 | Não | Não |
| LEG-08 | Como funciona o processo de mudança de perfil curricular em Sistemas de Informação? | SI/novo | Não | 0.223865 | Não | Não |
| LEG-09 | Qual o horário de funcionamento do restaurante universitário? | CC/novo | Sim | 0.334961 | Não | Não |
| LEG-10 | Como faço para solicitar bolsa de pós-graduação no CIn? | CC/novo | Sim | 0.334601 | Não | Não |
| PPC-CC-novo | Qual o perfil profissional do egresso de Ciência da Computação segundo o projeto pedagógico? | CC/novo | Não | 0.188336 | Não | Não |
| PPC-CC-anterior | Qual o perfil profissional do egresso de Ciência da Computação segundo o projeto pedagógico? | CC/anterior | Não | 0.227456 | Não | Não |
| PPC-EC-novo | Qual o perfil profissional do egresso de Engenharia da Computação segundo o projeto pedagógico? | EC/novo | Não | 0.211051 | Não | Não |
| PPC-EC-anterior | Qual o perfil profissional do egresso de Engenharia da Computação segundo o projeto pedagógico? | EC/anterior | Não | 0.183145 | Não | Não |
| PPC-SI-novo | Qual o perfil profissional do egresso de Sistemas de Informação segundo o projeto pedagógico? | SI/novo | Não | 0.202575 | Não | Não |
| PPC-SI-anterior | Qual o perfil profissional do egresso de Sistemas de Informação segundo o projeto pedagógico? | SI/anterior | Não | 0.222400 | Não | Não |
| PPC-IA-novo | Qual o perfil profissional do egresso de Inteligência Artificial segundo o projeto pedagógico? | IA/novo | Não | 0.244458 | Não | Não |
| FORA-01 | carburador | CC/novo | Sim | 0.728976 | Não | Sim |
| FORA-02 | Como consertar um carburador de motocicleta? | CC/novo | Sim | 0.453562 | Não | Não |
| FORA-03 | Qual a receita de bolo de chocolate? | CC/novo | Sim | 0.539267 | Não | Sim |
| FORA-04 | Qual a previsão do tempo em Marte? | CC/novo | Sim | 0.451403 | Não | Não |
| FORA-05 | Quem ganhou a Copa do Mundo de 1994? | CC/novo | Sim | 0.499876 | Não | Não |
| FORA-06 | Como trocar o pneu de uma bicicleta? | CC/novo | Sim | 0.373377 | Não | Não |
| FORA-07 | Qual o melhor investimento em criptomoedas? | CC/novo | Sim | 0.405665 | Não | Não |
| FORA-08 | Como renovar meu passaporte? | CC/novo | Sim | 0.542664 | Não | Sim |

## Interpretação e decisão

- Limiar 0,8: 15/25 decisões conforme expectativa; dez aceitações externas indevidas e nenhuma recusa dos 15 casos dentro do escopo.
- Limiar 0,5: 18/25 conforme; sete aceitações externas e nenhuma recusa interna.
- Sete controles recuperaram o PPC correspondente no top-3, incluindo curso/perfil. Isso não mede qualidade da resposta final.
- A pergunta curta carburador teve distância 0,728976: recusa com 0,5. A frase completa sobre conserto teve 0,453562: continua aceita com ambos. O print de Eric e a falha anterior podem, portanto, coexistir.
- Os nomes de fontes da planilha legada não correspondem literalmente aos arquivos atuais em vários casos. O texto de resposta esperado não é testável com mock. Não se declara recuperação exata das fontes legadas nem 100% de qualidade acadêmica.
- A primeira execução continha oráculo com letras maiúsculas nos nomes PPC-CC/EC/SI/IA. Corrigiu-se para nomes reais minúsculos, preservando benchmark-real/ e benchmark-casos-oraculo-inicial.json. A segunda execução está em benchmark-final/; a execução de entrega em benchmark-entrega/ acrescenta verificação da minuta visual sem mudar os casos. Perguntas, expectativas de fallback e limiares não mudaram.
- Amostra pequena, sem conjunto independente de validação e sem referência semântica completa. Não escolher limiar ideal a partir desses 25 casos. Mantém-se 0,8 provisório; QA-01 segue aberta, com plano de avaliação da recuperação/classificação de escopo.

## Interface

AppTest do Streamlit, sem navegador, enviou duas perguntas ao NestJS real. O estado de elementos comprova aviso mock, nomes com página e texto literal. Histórico também foi reexibido sem exceção. A resposta HTTP não foi inventada: somente a URL foi direcionada à porta temporária do ensaio. API pública: https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest

Não foi feita inspeção de pixels em navegador. Os processos temporários foram encerrados. Não foi enviado e-mail nem usada API paga de LLM.

A execução de entrega também confirmou, no AppTest ligado explicitamente ao backend com limiar 0,5, a mensagem de fallback e a minuta para carburador. Isso não muda o padrão de produção 0,8 nem valida a frase completa.
