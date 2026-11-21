import io
import json
import os
import unittest
from unittest.mock import patch

from src.generation import GenerationUnavailable, gerar_resposta


class OllamaGenerationTest(unittest.TestCase):
    contexto = 'O requerimento está em https://secgrad.cin.ufpe.br/requerimentos-e-documentos'

    @staticmethod
    def envelope(resposta, evidencias, reason='stop'):
        return io.BytesIO(json.dumps({
            'done': True, 'done_reason': reason,
            'message': {'content': json.dumps({'resposta': resposta, 'evidencias': evidencias})},
        }).encode())

    def test_usa_modelo_local_e_retorna_texto_com_evidencia(self):
        with patch.dict(os.environ, {'SECGRAD_GENERATION_MODE': 'ollama'}, clear=True), patch(
            'src.ollama_generation._LOCAL_HTTP.open', return_value=self.envelope(self.contexto, ['1'])
        ) as request:
            self.assertEqual(gerar_resposta('Onde encontro o formulário?', self.contexto), self.contexto)
        sent = request.call_args.args[0]
        self.assertEqual(sent.full_url, 'http://127.0.0.1:11434/api/chat')
        self.assertIsNone(sent.get_header('Authorization'))
        self.assertEqual(json.loads(sent.data)['model'], 'qwen3:4b')

    def test_abstem_se_quando_modelo_nao_tem_evidencia_ou_inventa_link(self):
        for resposta, evidencias in ((None, []), ('Acesse https://example.org', ['1']), ('Fonte inexistente', ['99']), ('Onde encontro o formulário?', ['1'])):
            with self.subTest(resposta=resposta), patch.dict(os.environ, {'SECGRAD_GENERATION_MODE': 'ollama'}, clear=True), patch(
                'src.ollama_generation._LOCAL_HTTP.open', return_value=self.envelope(resposta, evidencias)
            ):
                self.assertIsNone(gerar_resposta('Onde encontro o formulário?', self.contexto))

    def test_interrompido_ou_indisponivel_e_falha_tecnica(self):
        with patch.dict(os.environ, {'SECGRAD_GENERATION_MODE': 'ollama'}, clear=True):
            for params in ({'return_value': self.envelope(None, [], 'length')}, {'side_effect': TimeoutError}):
                with patch('src.ollama_generation._LOCAL_HTTP.open', **params), self.assertRaises(GenerationUnavailable):
                    gerar_resposta('Onde encontro o formulário?', self.contexto)

    def test_rejeita_endereco_externo(self):
        with patch.dict(os.environ, {'SECGRAD_GENERATION_MODE': 'ollama', 'SECGRAD_OLLAMA_URL': 'https://example.org'}, clear=True), patch(
            'src.ollama_generation._LOCAL_HTTP.open'
        ) as request, self.assertRaises(GenerationUnavailable):
            gerar_resposta('Onde encontro o formulário?', self.contexto)
        request.assert_not_called()
