"""Conferência adicional, sem sobrescrever o manifesto ou as evidências antigas."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def verificar():
    spec = importlib.util.spec_from_file_location('verificador_anterior', ROOT / 'docs/testes/verificar_entrega_sprint3.py')
    anterior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anterior)
    anterior.verificar()
    base = ROOT / 'docs/qualidade/IA-REF-04-evidencias'
    a = json.loads((base / 'antes/execucao.json').read_text(encoding='utf-8'))
    b = json.loads((base / 'depois/execucao.json').read_text(encoding='utf-8'))
    assert a['test_exit'] == b['test_exit'] == 0
    assert a['tests_sha256'] == b['tests_sha256']
    for phase in ['antes', 'depois']:
        log = (base / phase / 'execucao.txt').read_text(encoding='utf-8')
        assert 'Ran 21 tests' in log and '\nOK' in log
        assert (base / phase / 'html/index.html').exists()
    assert hashlib.sha256((ROOT / 'ai-service/src/retriever.py').read_bytes()).hexdigest() == {k.replace(chr(92), '/'): v for k, v in b['production_sha256'].items()}['ai-service/src/retriever.py']
    for nome_original in a['tests_sha256']:
        nome = nome_original.replace(chr(92), '/')
        old = subprocess.check_output(['git', 'show', f'c7c0e05:{nome}'], cwd=ROOT).replace(b'\r\n', b'\n')
        assert (ROOT / nome).read_bytes().replace(b'\r\n', b'\n') == old
    real = json.loads((HERE / 'servicos-reais/integracao-real.json').read_text(encoding='utf-8'))
    live = json.loads((HERE / 'servicos-reais/live-opt-in.json').read_text(encoding='utf-8'))
    assert real['sucesso'] and len(real['casos']) == 10 and real['processos_temporarios_encerrados']
    assert live['numPassedTests'] == 2 and live['numFailedTests'] == 0
    txt = (HERE / 'ia-regressao.txt').read_text(encoding='utf-8')
    assert 'Ran 20 tests' in txt and '\nOK' in txt
    pdfs = {'docs/testes/analise-critica-sprint3-reforco-20261110.pdf': 5,
            'docs/qualidade/relatorio-refatoracoes-sprint3-reforco-20261110.pdf': 3}
    for nome, count in pdfs.items():
        assert len(PdfReader(ROOT / nome).pages) == count
    indice = ROOT / 'docs/ENTREGA-SPRINT3.md'
    for link in re.findall(r'\]\(([^)]+)\)', indice.read_text(encoding='utf-8')):
        if not link.startswith(('https:', 'http:', '#')):
            assert (indice.parent / link.split('#')[0]).exists(), link
    paths = set(base.rglob('*')) | set(HERE.rglob('*'))
    paths |= {ROOT / p for p in pdfs}
    paths |= {indice, ROOT / 'docs/qualidade/divida-tecnica.md', ROOT / 'docs/qualidade/log-analise.md', ROOT / 'docs/testes/llm-log.md'}
    hashes = []
    for p in sorted(paths):
        if not p.is_file() or p.name == 'VERIFICACAO-REFORCO.json':
            continue
        raw = p.read_bytes()
        entry = {'arquivo': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest()}
        try:
            entry['sha256_utf8_lf'] = hashlib.sha256(raw.decode('utf-8').replace('\r\n', '\n').encode('utf-8')).hexdigest()
        except UnicodeDecodeError:
            pass
        hashes.append(entry)
    return {'status': 'reforco_verificado_com_ressalvas_historicas', 'v2_academica_antes': 21, 'v2_academica_depois': 21,
        'suite_identica': True, 'commit_refatoracao': 'c0f7116', 'pdf_paginas': pdfs, 'manifesto': hashes,
        'itens_academicos_principais': ['BACK-REF-01', 'IA-REF-02', 'IA-REF-04'],
        'complemento': 'BACK-REF-03',
        'limites': ['Prompt histórico e snapshot exato indisponíveis.', 'Teto de branches do backend permanece declarado.',
                   'Benchmark anterior preservado, sem calibração ou LLM real.', 'Revisão humana e envio não certificados.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', type=Path)
    a = p.parse_args()
    d = verificar()
    if a.saida:
        if a.saida.exists():
            p.error('Use destino novo para preservar o registro anterior.')
        a.saida.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: d[k] for k in ['status', 'v2_academica_antes', 'v2_academica_depois', 'suite_identica', 'pdf_paginas']}, ensure_ascii=False))
