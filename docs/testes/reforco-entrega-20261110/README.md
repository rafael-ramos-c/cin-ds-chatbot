# Reforço da entrega - V2 acadêmica e auditoria documental

Base publicada: c7c0e05 (PR #37). Nova branch local: test/reforco-v2-academica-sprint3.
Esta rodada não refaz a V1 nem reescreve resultados históricos.

## Melhoria principal

IA-REF-04 separa a leitura/validação das fontes da montagem de contexto no retriever.
Antes de alterar: mesmos 21 testes da V2 acadêmica US-01 aprovados, registro c93450a;
HTML incluído em c9328fe porque o diretório de cobertura é ignorado por padrão.
Alteração isolada em c0f7116; depois, os mesmos 21 métodos aprovados, mesmos hashes.
Escopo idêntico src.retriever + src.metadata_utils, coverage.py 7.17.0 com branches.
Linhas 93/97 -> 96/100; branches 41/42 em ambos. Mudança estrutural não é novo
comportamento testado. V1/V2 não foram editadas, nem seus denominadores históricos.

Agora há três itens principais diretamente protegidos pelas V2 da Parte 1:
BACK-REF-01, IA-REF-02 e IA-REF-04. BACK-REF-03 é evidência complementar com regressão
corrente; a diferença deixa de ser a única proteção do terceiro item exigido.

## Checagens desta rodada

- V2 acadêmica antes/depois: 21/21, hashes iguais, JSON e HTML em
  ../../qualidade/IA-REF-04-evidencias/antes e depois.
- Regressão IA: 20/20, ia-regressao.txt.
- Integração posterior: dez chamadas HTTP e dois testes opt-in aprovados,
  servicos-reais/. Corpus real, geração mock, processos temporários encerrados.
- Benchmark de 25 casos, 256 testes backend e 12 UI são evidências da rodada
  anterior preservada, não foram anunciados como reexecutados aqui. Não houve
  mudança no backend, UI, filtros, consulta, embeddings ou corpus nesta extração.
- PDFs com reforco-20261110: análise cinco páginas e refatorações três páginas,
  renderizados e conferidos. Versões anteriores não foram substituídas.
- AUDITORIA-CRITERIOS.md distingue material disponível de ressalvas e ações humanas.

## Reprodução

Em ai-service, com o ambiente Python do projeto:

```powershell
python scripts/medir_us01.py v2 DESTINO_NOVO
python -m unittest discover -s tests -v
```

Na raiz, Node 24 no PATH e backend compilado:

```powershell
python backend/scripts/verificar-integracao-real.py --saida docs/testes/ensaio-novo-reforco
python docs/testes/reforco-entrega-20261110/verificar_reforco.py
```

Não executar o medidor em antes/depois existentes. Não sobrescrever históricos.
Para a entrega, seguir ../../ENTREGA-SPRINT3.md e usar os arquivos com reforco no nome.
Não há aprovação da professora ou revisão humana do grupo criada pelo assistente.
