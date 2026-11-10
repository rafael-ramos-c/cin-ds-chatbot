# Manual do Desenvolvedor — Serviço de IA/RAG

## 1. Objetivo

O `ai-service` é o microsserviço responsável pela recuperação de
informações acadêmicas utilizadas pelo Chatbot SecGrad.

Suas responsabilidades atuais são:

- processar documentos PDF e TXT;
- dividir o conteúdo em trechos;
- gerar e armazenar embeddings no ChromaDB;
- filtrar documentos por curso e perfil curricular;
- recuperar trechos semanticamente relacionados à pergunta;
- devolver contexto, fontes e distância para o backend NestJS.

O contrato de geração está implementado: `POST /api/v1/gerar`, entrada
`pergunta`/`contexto`, saída `resposta` textual ou nula. O provedor real ainda
não está implementado; sem `SECGRAD_GENERATION_MODE=mock`, contexto não vazio
produz HTTP 503. O modo mock não é resposta acadêmica.

## 2. Estrutura principal

```text
ai-service/
├── main.py
├── requirements.txt
├── chroma_db/
├── src/
│   ├── config.py
│   ├── index_utils.py
│   ├── ingest.py
│   ├── ingest_batch.py
│   ├── metadata_utils.py
│   ├── retriever.py
│   └── validate_catalog.py
└── tests/
    ├── __init__.py
    ├── test_index_utils.py
    ├── test_metadata_utils.py
    └── test_retriever.py
```

Os módulos `generation.py`, os testes de geração, `scripts/validar_base_documental.py`
e `tests/test_ingest_pages.py` complementam essa estrutura. As suítes históricas
ficam em `tests/v1-llm` e `tests/v2`; não devem ser substituídas por regressões novas.

## 3. Preparação no Windows / PowerShell

Na raiz do repositório (Python instalado e ambiente virtual existente):

```powershell
.\venv\Scripts\Activate.ps1
python -m pip install -r .\ai-service\requirements-dev.txt
```

Se não houver ambiente: `python -m venv venv`, antes da ativação. A interface
também precisa de `python -m pip install streamlit pandas openpyxl requests`.
Node.js 24 e npm são necessários para o NestJS.

## 4. Catálogo e ingestão (terminal na pasta ai-service)

```powershell
cd ai-service
python -m src.validate_catalog
python -m src.ingest_batch
python -m scripts.validar_base_documental --saida ../docs/testes/validacao-ppcs/auditoria-nova.json
```

O último comando usa uma saída nova e somente lê a coleção existente; não cria
uma base vazia nem reescreve evidências antigas. Não executar `ingest.py` diretamente:
esse arquivo define funções, enquanto `src.ingest_batch` processa o catálogo.

Dados canônicos: `data/raw/metadata.json` e documentos na mesma pasta. `ai-service/data`
é legado. `fonttools` auxilia fontes PDF; não faz OCR. Páginas sem texto são avisadas
e continuam ausentes da busca. Não confundir sucesso de um documento com extração
completa de todas as páginas. O número citado é a posição física da página no PDF.

Reingestão usa IDs determinísticos e upsert. Para cada documento processado remove
IDs obsoletos daquele documento; não remove automaticamente documentos retirados do
catálogo. Não apagar `chroma_db` para atualizar os PPCs. Antes de manutenção, parar
os serviços e preservar uma cópia da base.

## 5. Execução em três terminais

Terminal 1, em `ai-service`, após a ingestão:

```powershell
$env:SECGRAD_GENERATION_MODE='mock'
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Terminal 2, em `backend`:

```powershell
npm ci
$env:AI_SERVICE_URL='http://127.0.0.1:8000'
$env:AI_SERVICE_TIMEOUT_MS='30000'
npm run start:dev
```

O timeout ampliado é de desenvolvimento, por chamada. O padrão é 5000 ms; inicialização
do modelo de embeddings pode demorar mais na primeira busca. Não enfraquecer validações
de URL para contornar configuração ausente. Em 08/11 foi restaurado o contrato:
`AI_SERVICE_URL` explícita é obrigatória; não há localhost padrão. Ver
[fechamento do backend](testes/fechamento-backend-20261108/README.md).

Terminal 3, na raiz, com o ambiente Python ativado:

```powershell
python -m streamlit run app.py
```

Interface: http://localhost:8501. Saúde: http://127.0.0.1:8000/health.
API documentada do serviço de IA: http://127.0.0.1:8000/docs.

## 6. Testes e limitações

Na pasta `ai-service`:

```powershell
python -m unittest discover -s tests -v
python -m unittest discover -s tests/v2 -v
```

A validação da base real é opt-in e independente das suítes V1/V2; registra versão,
hashes dos documentos, trechos, páginas e consultas nos sete pares curso/perfil.
Ela não prova qualidade de respostas por LLM, não calibra o limiar 0.8 e não substitui
o benchmark do Eric. Erros 503 podem vir de conexão/configuração ou da geração
desabilitada; 504 indica timeout. Contexto de busca não é resposta gerada.

Variáveis do RAG: `SECGRAD_DATA_DIR`, `SECGRAD_CHROMA_PATH`, `SECGRAD_COLLECTION`.
Defini-las antes de iniciar o processo; defaults estão em `src/config.py`.
Resultados atuais e lacunas para Ricardo/Eric/Victor:
[Validação dos PPCs](testes/validacao-ppcs/README.md).


## Revisão pós-OCR de 09/11/2026

A base local foi reingerida após o PR #35: 21 documentos e 6.811 trechos,
sem divergências contra a extração atual, com sete pares curso/perfil verificados.
Quatro páginas de SI ganharam texto; EC anterior, página física 22, continua sem
extração. Ver [evidências e reprodução](testes/validacao-pos-ocr-20261109/README.md).
Cada integrante precisa reingerir a base local após atualizar os PDFs: o ChromaDB
não é enviado ao Git. A integração foi testada com geração mock, não LLM real.


## Fechamento de 10/11/2026

[Entrega e reprodução](ENTREGA-SPRINT3.md). O limiar padrão foi restaurado para
0,8; para testar explicitamente 0,5, usar FALLBACK_DISTANCE_THRESHOLD no processo
NestJS, sem declarar calibração. A fonte literal na UI é associada ao cabeçalho
arquivo/página/curso de contexto; se a associação não é verificável, não há citação
inventada. Essa dependência textual está registrada como API-01 para evolução.

Benchmark: na raiz, executar `python scripts/benchmark_sprint3.py --casos docs/testes/fechamento-final-20261110/benchmark-casos.json --saida docs/testes/novo-benchmark`.
Requer Node 24, backend compilado, ambiente Python do projeto e ChromaDB ingerido.
Cria e encerra serviços em portas temporárias, gera respostas mock e usa AppTest,
sem navegador. Não usar resultado de infraestrutura como métrica de qualidade.
