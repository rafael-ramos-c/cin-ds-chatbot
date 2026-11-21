import io
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import URLError

from fastapi.testclient import TestClient

from main import app


class OpenAIGenerationTest(unittest.TestCase):
    contexto = "O formulário oficial está em https://secgrad.cin.ufpe.br/requerimentos-e-documentos"

    def setUp(self):
        self.client = TestClient(app)
        env = patch.dict(os.environ, {
            "SECGRAD_GENERATION_MODE": "openai", "SECGRAD_OPENAI_MODEL": "gpt-5.4-mini",
            "OPENAI_API_KEY": "chave-ficticia",
        }, clear=True)
        env.start()
        self.addCleanup(env.stop)

    def gerar(self):
        return self.client.post("/api/v1/gerar", json={"pergunta": "Onde fica o formulário?", "contexto": self.contexto})

    @staticmethod
    def resposta_provedor(resposta, evidencias):
        texto = json.dumps({"resposta": resposta, "evidencias": evidencias})
        return io.BytesIO(json.dumps({"status": "completed", "output": [
            {"type": "reasoning"},
            {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": texto}]},
        ]}).encode())

    def test_resposta_com_evidencia_literal_e_configuracao_do_pedido(self):
        with patch("src.openai_generation.urlopen", return_value=self.resposta_provedor(self.contexto, [self.contexto])) as obter:
            response = self.gerar()
        self.assertEqual(response.json(), {"resposta": self.contexto})
        requisicao = obter.call_args.args[0]
        enviado = json.loads(requisicao.data)
        self.assertEqual(requisicao.full_url, "https://api.openai.com/v1/responses")
        self.assertEqual(requisicao.get_header("Authorization"), "Bearer chave-ficticia")
        self.assertFalse(enviado["store"])
        self.assertEqual(json.loads(enviado["input"])["trechos"], self.contexto)
        self.assertTrue(enviado["text"]["format"]["strict"])

    def test_insuficiencia_e_fontes_inventadas_resultam_em_null(self):
        for resposta, citacoes in ((None, []), ("Prazo de sete dias", ["Prazo de 7 dias"]),
                                   ("Acesse https://example.com/form", [self.contexto]), ("Sem fonte", [])):
            with self.subTest(resposta=resposta), patch(
                "src.openai_generation.urlopen", return_value=self.resposta_provedor(resposta, citacoes)
            ):
                response = self.gerar()
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"resposta": None})

    def test_erros_do_provedor_nao_expoem_detalhes(self):
        with patch("src.openai_generation.urlopen", side_effect=URLError("detalhe confidencial")):
            response = self.gerar()
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"detail": "Serviço de geração indisponível."})

    def test_sem_chave_nao_faz_pedido(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}), patch("src.openai_generation.urlopen") as obter:
            response = self.gerar()
        self.assertEqual(response.status_code, 503)
        obter.assert_not_called()

    def test_saida_incompleta_e_falha_tecnica(self):
        incompleta = io.BytesIO(b'{"status": "incomplete", "output": []}')
        with patch("src.openai_generation.urlopen", return_value=incompleta):
            self.assertEqual(self.gerar().status_code, 503)
