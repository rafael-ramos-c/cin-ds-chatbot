"""Benchmark observacional reproduzível: corpus real, geração mock, sem calibrar automaticamente."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from unittest.mock import patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def executar(casos_path, saida):
    processos, logs = [], []
    resultado = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'node': subprocess.check_output(['node', '--version'], text=True).strip(),
        'casos_sha256': hashlib.sha256(casos_path.read_bytes()).hexdigest(),
        'modo': 'mock', 'casos': [], 'infraestrutura_ok': False,
        'versoes': {p: importlib.metadata.version(p) for p in ['chromadb', 'pypdf', 'streamlit']},
        'documentos_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / 'data/raw').glob('*')) if p.is_file()},
        'limites': ['Não mede qualidade de resposta de LLM real.', 'Não seleciona limiar ideal; amostra pequena e sem representatividade estatística.', 'AppTest verifica elementos, não pixels em navegador.'],
    }

    def porta():
        with socket.socket() as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]

    def iniciar(cmd, cwd, env, nome, health):
        log = (saida / (nome + '.txt')).open('w', encoding='utf-8')
        logs.append(log)
        processo = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT,
                                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        processos.append(processo)
        prazo = time.monotonic() + 45
        while time.monotonic() < prazo:
            if processo.poll() is not None:
                raise RuntimeError(f'{nome} encerrou; conferir log.')
            try:
                if requests.get(health, timeout=1).status_code == 200:
                    return
            except requests.RequestException:
                pass
            time.sleep(.25)
        raise TimeoutError(f'{nome} não iniciou em 45s.')

    def post(url, body):
        r = requests.post(url, json=body, timeout=65)
        if r.status_code not in (200, 201):
            raise RuntimeError(f'HTTP {r.status_code}: {r.text[:300]}')
        return r.json()

    try:
        ai = f'http://127.0.0.1:{porta()}'
        env = dict(os.environ, PYTHONUTF8='1', SECGRAD_GENERATION_MODE='mock')
        iniciar([sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', ai.rsplit(':', 1)[1]], ROOT / 'ai-service', env, 'fastapi', ai + '/health')
        casos = json.loads(casos_path.read_text(encoding='utf-8'))['casos']
        # Aquecer a coleção antes de aplicar timeout do backend.
        primeiro = casos[0]
        post(ai + '/api/v1/buscar', {k: primeiro[k] for k in ['pergunta', 'curso', 'perfil']})
        backends = {}
        for limiar in ['0.8', '0.5']:
            url = f'http://127.0.0.1:{porta()}'
            env = dict(os.environ, AI_SERVICE_URL=ai, PORT=url.rsplit(':', 1)[1], AI_SERVICE_TIMEOUT_MS='30000', FALLBACK_DISTANCE_THRESHOLD=limiar)
            iniciar(['node', 'dist/main.js'], ROOT / 'backend', env, 'nestjs-' + limiar, url + '/')
            backends[limiar] = url
        for caso in casos:
            consulta = {k: caso[k] for k in ['pergunta', 'curso', 'perfil']}
            consulta['top_k'] = 3
            linha = {'caso': caso, 'resultados': {}}
            for limiar, url in backends.items():
                inicio = time.monotonic()
                r = post(url + '/api/v1/conversa', {'consulta': consulta})
                fontes = r.get('fontes', [])
                isolado = all(f['arquivo'] in resultado['documentos_sha256'] and isinstance(f['pagina'], int) and f['pagina'] >= 1 for f in fontes)
                linha['resultados'][limiar] = {
                    'distancia_minima': r['distancia_minima'], 'fallback': r['fallback_acionado'],
                    'fallback_conforme_expectativa': r['fallback_acionado'] == caso['fallback_esperado'],
                    'fontes': fontes, 'contexto': r['contexto'], 'resposta': r.get('resposta'),
                    'template_email': r.get('template_email'), 'setor_sugerido': r.get('setor_sugerido'),
                    'citacoes_com_arquivo_e_pagina': isolado,
                    'fonte_esperada_recuperada': any(f['arquivo'] == caso['fonte_esperada'] for f in fontes) if 'fonte_esperada' in caso else None,
                    'segundos': round(time.monotonic() - inicio, 3),
                }
            resultado['casos'].append(linha)
            print(caso['id'], 'medido', flush=True)
        resultado['resumo'] = {}
        for limiar in backends:
            r = [x['resultados'][limiar] for x in resultado['casos']]
            resultado['resumo'][limiar] = {'total': len(r), 'fallback_conforme': sum(x['fallback_conforme_expectativa'] for x in r),
                'falsos_positivos_recuperacao': sum(not x['resultados'][limiar]['fallback'] and x['caso']['fallback_esperado'] for x in resultado['casos']),
                'recusas_em_casos_dentro_escopo': sum(x['resultados'][limiar]['fallback'] and not x['caso']['fallback_esperado'] for x in resultado['casos'])}

        from streamlit.testing.v1 import AppTest
        import src.ui.api_client as cliente
        ui = {'metodo': 'AppTest headless com chamadas HTTP reais ao NestJS; apenas URL redirecionada para porta temporária.'}
        anterior = Path.cwd()
        os.chdir(ROOT)
        try:
            with patch.object(cliente, 'NESTJS_API_URL', backends['0.8'] + '/api/v1/conversa'):
                at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=60).run()
                assert not at.exception, str(at.exception)
                q = next(c for c in casos if c['id'] == 'PPC-CC-novo')['pergunta']
                at.chat_input[0].set_value(q).run(timeout=60)
                assert not at.exception, str(at.exception)
                ui['markdown'] = [x.value for x in at.markdown]
                ui['trechos_texto'] = [x.value for x in at.text]
                ui['aviso_mock_visivel'] = any('[SIMULAÇÃO DE INTEGRAÇÃO' in x for x in ui['markdown'])
                ui['pagina_visivel'] = any('(pág.' in x for x in ui['markdown'])
                ui['trecho_literal_visivel'] = bool(ui['trechos_texto'])
                assert ui['aviso_mock_visivel'] and ui['pagina_visivel'] and ui['trecho_literal_visivel']
                # O segundo envio também exercita a renderização do histórico.
                at.chat_input[0].set_value('carburador').run(timeout=60)
                assert not at.exception, str(at.exception)
                ui['segundo_envio_sem_excecao'] = True
                # Verificar o ramo visual de fallback em cenário explicitamente 0,5.
                with patch.object(cliente, 'NESTJS_API_URL', backends['0.5'] + '/api/v1/conversa'):
                    at.chat_input[0].set_value('carburador').run(timeout=60)
                    assert not at.exception, str(at.exception)
                    textos = [x.value for x in at.markdown]
                    ui['fallback_visual_limiar_05'] = any('evidências suficientes' in x and 'Setor Recomendado' in x for x in textos)
                    ui['minuta_visual_limiar_05'] = any('Assunto:' in x and 'carburador' in x for x in textos)
                    assert ui['fallback_visual_limiar_05'] and ui['minuta_visual_limiar_05']
        finally:
            os.chdir(anterior)
        resultado['ui'] = ui
        resultado['infraestrutura_ok'] = True
    except Exception as erro:
        resultado['erro'] = f'{type(erro).__name__}: {erro}'
    finally:
        for processo in reversed(processos):
            if processo.poll() is None:
                processo.terminate()
            try:
                processo.wait(timeout=10)
            except subprocess.TimeoutExpired:
                processo.kill()
                processo.wait()
        for log in logs:
            log.close()
        resultado['processos_temporarios_encerrados'] = True
        (saida / 'benchmark.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding='utf-8')
    return resultado


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--casos', required=True, type=Path)
    p.add_argument('--saida', required=True, type=Path)
    a = p.parse_args()
    a.saida.mkdir(parents=True, exist_ok=False)
    r = executar(a.casos.resolve(), a.saida.resolve())
    print(json.dumps({'infraestrutura_ok': r['infraestrutura_ok'], 'resumo': r.get('resumo'), 'erro': r.get('erro')}, ensure_ascii=False))
    raise SystemExit(0 if r['infraestrutura_ok'] else 1)
