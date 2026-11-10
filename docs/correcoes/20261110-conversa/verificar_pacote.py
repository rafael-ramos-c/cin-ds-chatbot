"""Confere arquivos e resultados desta revisão; não executa novamente os testes."""
from pathlib import Path
import hashlib
import json
import re
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def verificar():
    for arquivo, total in [('testes-ui.txt', 18), ('testes-ia.txt', 27), ('testes-v2.txt', 21)]:
        texto = (HERE / arquivo).read_text(encoding='utf-8')
        assert f'Ran {total} tests' in texto and '\nOK' in texto, arquivo
    integracao = json.loads((HERE / 'integracao.json').read_text(encoding='utf-8'))
    assert integracao['sucesso'] and 'Não encontrei um endereço' in integracao['resposta']
    assert any('regras_requerimentos' in s['documento'] for s in integracao['fontes'])
    app = json.loads((HERE / 'apptest.json').read_text(encoding='utf-8'))
    assert app['sem_excecoes'] and app['historico_limpo_ao_trocar_curso']
    pdfs = {'docs/testes/analise-critica-sprint3-conversa-20261110.pdf': 5,
            'docs/qualidade/relatorio-refatoracoes-sprint3-conversa-20261110.pdf': 3}
    for p, n in pdfs.items():
        assert len(PdfReader(ROOT / p).pages) == n
    # Fonte V2 não editada desde a medição acadêmica anterior.
    anterior = json.loads((ROOT / 'docs/qualidade/IA-REF-04-evidencias/depois/execucao.json').read_text(encoding='utf-8'))
    for caminho, sha in anterior['tests_sha256'].items():
        assert hashlib.sha256((ROOT / caminho.replace('\\', '/')).read_bytes()).hexdigest() == sha
    indice = ROOT / 'docs/ENTREGA-SPRINT3.md'
    for link in re.findall(r'\]\(([^)]+)\)', indice.read_text(encoding='utf-8')):
        if not link.startswith(('http:', 'https:', '#')):
            assert (indice.parent / link.split('#')[0]).exists(), link
    arquivos = set(HERE.rglob('*')) | set((ROOT / 'docs/correcoes/20261110-texto-pdf').rglob('*'))
    arquivos |= {ROOT / p for p in pdfs}
    arquivos |= {ROOT / p for p in ['app.py', 'src/ui/api_client.py', 'src/ui/conversation.py',
        'ai-service/src/ingest.py', 'ai-service/src/pdf_text.py', 'ai-service/src/retriever.py',
        'tests/ui/test_conversation.py', 'ai-service/tests/test_pdf_text.py', 'ai-service/tests/test_topic_filter.py']}
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(arquivos) if p.is_file() and p.name != 'VERIFICACAO.json' and '__pycache__' not in p.parts}
    return {'status': 'conferido_com_limites_documentados', 'pdf_paginas': pdfs,
            'testes': {'ui': 18, 'ia': 27, 'v2_historica': 21}, 'historico_v1_v2_preservado': True,
            'backend_e_benchmark_completo': 'não reexecutados nesta revisão', 'sha256': hashes}


if __name__ == '__main__':
    resultado = verificar()
    destino = HERE / 'VERIFICACAO.json'
    if destino.exists():
        raise SystemExit('O manifesto já existe; não sobrescrever evidência anterior.')
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Pacote conferido: PDFs 5 + 3 páginas; testes registrados 18 UI, 27 IA e 21 V2.')
