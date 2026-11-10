"""Verifica artefatos da entrega sem reexecutar ou reescrever resultados históricos."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
FINAL = ROOT / 'docs/testes/fechamento-final-20261110'


def ler(path):
    return json.loads(path.read_text(encoding='utf-8'))


def verificar():
    ref = ROOT / 'docs/qualidade/BACK-REF-03-evidencias'
    antes, depois = ler(ref / 'antes/vitest-results.json'), ler(ref / 'depois/vitest-results.json')
    assert antes['numPassedTests'] == depois['numPassedTests'] == 256
    assert antes['numFailedTests'] == depois['numFailedTests'] == 0
    frozen = ler(ref / 'antes/estado.json')
    for item in frozen['tests']:
        raw = (ROOT / item['arquivo']).read_bytes().replace(b'\r\n', b'\n')
        assert hashlib.sha256(raw).hexdigest() == item['sha256_lf'], item['arquivo']
    config = (ROOT / 'backend/vitest.back-ref03.config.mts').read_bytes().replace(b'\r\n', b'\n')
    assert hashlib.sha256(config).hexdigest() == frozen['config']['sha256_lf']

    for nome, total, pending in [('backend-unitarios-corrigidos.json', 256, 0), ('backend-e2e.json', 34, 2), ('geracao-52.json', 52, 0)]:
        d = ler(FINAL / nome)
        assert d['numPassedTests'] == total and d['numFailedTests'] == 0 and d['numPendingTests'] == pending, nome
    for nome, total in [('ia-regressao.txt', 20), ('ia-v2.txt', 21), ('ui-unitarios.txt', 12)]:
        txt = (FINAL / nome).read_text(encoding='utf-8')
        assert f'Ran {total} tests' in txt and '\nOK' in txt, nome
    real = ler(FINAL / 'servicos-reais/integracao-real.json')
    live = ler(FINAL / 'servicos-reais/live-opt-in.json')
    assert real['sucesso'] and len(real['casos']) == 10 and real['processos_temporarios_encerrados']
    assert live['numPassedTests'] == 2 and live['numFailedTests'] == 0

    bench = ler(FINAL / 'benchmark-entrega/benchmark.json')
    assert bench['infraestrutura_ok'] and len(bench['casos']) == 25 and bench['processos_temporarios_encerrados']
    for campo in ['aviso_mock_visivel', 'pagina_visivel', 'trecho_literal_visivel', 'segundo_envio_sem_excecao', 'fallback_visual_limiar_05', 'minuta_visual_limiar_05']:
        assert bench['ui'][campo], campo
    assert hashlib.sha256((FINAL / 'benchmark-casos.json').read_bytes()).hexdigest() == bench['casos_sha256']
    ppcs = [c for c in bench['casos'] if c['caso']['grupo'] == 'controle_documental']
    assert len(ppcs) == 7 and all(c['resultados']['0.8']['fonte_esperada_recuperada'] for c in ppcs)

    audit = ler(ROOT / 'docs/testes/validacao-pos-ocr-20261109/auditoria-final.json')
    assert audit['total_trechos'] == 6811 and not audit['erros']
    for item in audit['documentos']:
        assert hashlib.sha256((ROOT / 'data/raw' / item['arquivo']).read_bytes()).hexdigest() == item['sha256']

    protegidos = ['ai-service/tests', 'backend/test/sprint3-v2', 'tests/v1-llm', 'tests/v2']
    assert not subprocess.check_output(['git', 'diff', '--name-only', 'cd583e4', '--', *protegidos], cwd=ROOT, text=True).strip()
    paginas = {'docs/testes/analise-critica-sprint3-final-20261110.pdf': 5,
               'docs/qualidade/relatorio-refatoracoes-sprint3-final-20261110.pdf': 3}
    for path, total in paginas.items():
        assert len(PdfReader(ROOT / path).pages) == total
    indice = ROOT / 'docs/ENTREGA-SPRINT3.md'
    for destino in re.findall(r'\]\(([^)]+)\)', indice.read_text(encoding='utf-8')):
        if not destino.startswith(('http:', 'https:', '#')):
            assert (indice.parent / destino.split('#')[0]).exists(), destino

    paths = set(FINAL.rglob('*')) | set(ref.rglob('*'))
    paths.update(ROOT / x for x in paginas)
    paths.update(ROOT / x for x in ['app.py', 'src/ui/api_client.py', 'backend/src/ai-service/ai-service.service.ts',
        'backend/src/orchestration/fallback.config.ts', 'scripts/benchmark_sprint3.py', 'tests/ui/test_api_client.py',
        'docs/qualidade/divida-tecnica.md', 'docs/qualidade/log-analise.md', 'docs/testes/llm-log.md',
        'docs/testes/matriz-rastreabilidade.md', 'docs/ENTREGA-SPRINT3.md'])
    manifesto = []
    for path in sorted(paths):
        if not path.is_file() or path.name == 'VERIFICACAO-FINAL.json':
            continue
        raw = path.read_bytes()
        row = {'arquivo': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest()}
        try:
            row['sha256_utf8_lf'] = hashlib.sha256(raw.decode('utf-8').replace('\r\n', '\n').encode('utf-8')).hexdigest()
        except UnicodeDecodeError:
            pass
        manifesto.append(row)
    return {'utc': datetime.now(timezone.utc).isoformat(), 'status': 'artefatos_verificados_com_ressalvas_documentadas',
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'node': bench['node'], 'paginas_pdf': paginas, 'suite_identica_antes_depois': True,
        'historicos_preservados': True, 'corpus_inalterado_desde_auditoria_6811': True,
        'benchmark': bench['resumo'], 'manifesto': manifesto,
        'ressalvas': ['Geração mock e teste UI headless; sem LLM real ou inspeção de pixels em navegador.',
            'QA-01 aberta: falsos positivos de escopo; limiar 0,8 não calibrado.',
            'Prompt V2 integral e snapshot exato históricos do backend indisponíveis.',
            'V1 backend no teto de branches; meta estrita de aumento não atingível no mesmo recorte.',
            'BACK-REF-03 usa V2 de regressão corrente, distinta da V2 acadêmica histórica.',
            'Revisão humana, publicação dos commits e envio à professora não certificados.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--saida', type=Path)
    a = p.parse_args()
    d = verificar()
    if a.saida:
        if a.saida.exists():
            p.error('Use destino novo para preservar o manifesto anterior.')
        a.saida.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: d[k] for k in ['status', 'suite_identica_antes_depois', 'historicos_preservados', 'paginas_pdf', 'benchmark']}, ensure_ascii=False))
