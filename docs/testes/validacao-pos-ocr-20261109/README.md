# Validação pós-OCR - 09/11/2026

Base de produção: b40c4f43f055d704462efa02074d7413a0e0092d, após PRs #34 e #35.
Rafael executou esta rodada de IA/RAG e fechamento restante do backend.
Não é uma nova V1, terceira refatoração, benchmark de UI ou uso de LLM real.

## O que foi realizado

1. Backup local do ChromaDB antes da atualização (fora do repositório).
2. Comparação dos três PDFs com a revisão 69b2587: quatro páginas de SI ganharam
texto extraível; EC anterior, página física 22, continua vazia para o pypdf.
As quantidades de páginas foram preservadas. Ver ocr-comparacao.json.
3. Validação do catálogo e reingestão completa: ingestao.txt, 21/21 documentos.
4. Auditoria após o fim da ingestão: auditoria-final.json e
   auditoria-final-execucao.txt. Compara IDs, texto, metadados, páginas e
   documentos com a extração atual e testa sete pares de curso/perfil.
5. Regressões: regressao-ia-validada.txt, v2-atual.txt, backend-unitarios.json e
   backend-e2e.json. Os dois testes opt-in são executados separadamente no ensaio.
6. Integração real: servicos-reais/integracao-real.json e live-opt-in.json,
   com FastAPI/ChromaDB/NestJS reais e geração explicitamente mock.
7. Governança revisada em ../../qualidade/divida-tecnica.md e log-analise.md;
   novos PDFs datados de 09/11 preservam versões anteriores.

## Resultado final conferido

| Verificação | Resultado |
| --- | --- |
| Catálogo / ingestão | 21/21 documentos |
| ChromaDB / extração atual | 6.811/6.811 trechos, sem IDs extras ou divergências |
| Filtros e fontes | Sete pares curso/perfil conferidos |
| Páginas sem texto | Somente EC anterior, página 22 |
| Regressões IA / V2 US-01 | 20/20 e 21/21 |
| Backend corrente | 256/256 unitários; 34/34 e2e comuns |
| Serviços reais | Dez cenários HTTP e dois testes opt-in aprovados |

Antes do OCR eram 6.799 trechos; agora são 6.811. O aumento de 12 é fragmentação
resultante do texto atual, não uma métrica de qualidade ou cobertura de testes.
VERIFICACAO.json consolida as checagens e hashes dos arquivos desta rodada.

## Reprodução

Na raiz, com o ambiente Python do projeto e Node.js 24:

```powershell
.\venv\Scripts\Activate.ps1
cd ai-service
python -m src.validate_catalog
python -u -m src.ingest_batch
python -u -m scripts.validar_base_documental --saida ../docs/testes/auditoria-nova.json
python -m unittest discover -s tests -v
python -m unittest discover -s tests/v2 -p test_busca_v2.py -v
cd ..
python backend/scripts/verificar-integracao-real.py --saida docs/testes/ensaio-pos-ocr-novo
```

Use destinos novos: os verificadores recusam sobrescrever evidências. Para usar a
UI, siga os três terminais do README da raiz; as instâncias temporárias deste
ensaio foram encerradas. Cada computador precisa reingerir sua própria base:
o diretório ai-service/chroma_db é local e não faz parte deste commit.

## Limites e tentativas interrompidas

A primeira tentativa de unittest no ambiente restrito ficou presa ao iniciar
os testes HTTP locais; foi interrompida e repetida com comunicação local liberada.
regressao-ia.txt também terminou aprovada, mas a execução canônica desta rodada
é regressao-ia-validada.txt. A primeira auditoria foi interrompida para aguardar o
fim da gravação: auditoria-interrompida.txt é somente log parcial, sem valor de
certificação. Apenas auditoria-final.json representa a auditoria final.
A saída antiga de ingestão pode exibir acentos substituídos pela codificação do
terminal Windows; ela não é o texto documental usado na auditoria JSON UTF-8.

Extração completa contra os chunks não certifica reconhecimento OCR correto,
semântica das respostas, calibração de 0,8 ou interface. Não há LLM real neste
ensaio. O caso de carburador e os problemas de apresentação continuam no backlog.
Não foram removidos documentos duplicados nem alterados testes históricos,
contratos HTTP, backend de produção ou código de Eric nesta rodada.

## Próximos responsáveis

- Eric: validar UI, resposta/contexto/fontes, benchmark positivo/negativo e terceira
  refatoração formal com V2 antes/depois, ID e commit identificável.
- Ricardo: conferir EC22, fidelidade das quatro páginas de OCR e relação ano/perfil;
  revisar as dívidas e o log com a equipe, sem marcar duplicação como resolvida.
- Rafael (incluindo fechamento de Victor): incorporar os resultados de Eric e
  eventuais PDFs corrigidos, repetir validação afetada e finalizar os dois PDFs.
- Victor: pode complementar registros históricos reais de prompts se disponíveis;
  sua indisponibilidade fica explícita quando não houver material recuperável.

A análise crítica tem cinco páginas. O relatório de refatorações tem três,
mas permanece parcial (duas de três refatorações comprovadas).
