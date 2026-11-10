"""Regressão atual da UI; não substitui V1/V2 acadêmicas históricas."""
import unittest
from unittest.mock import Mock, patch

from src.ui.api_client import enviar_pergunta, extrair_trechos


FONTE = {"arquivo": "norma.pdf", "pagina": 2, "curso": "CC"}
CABECALHO = "[Documento: norma.pdf | Pág. 2 | Curso: CC]\n"
MARCADOR = "[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]"


class ClienteUiTest(unittest.TestCase):
    def chamar(self, data, status=201):
        response = Mock(status_code=status, text="erro técnico")
        response.json.return_value = data
        with patch("src.ui.api_client.requests.post", return_value=response) as post:
            resultado = enviar_pergunta(" Pergunta ", "CC", "novo")
            self.assertEqual(post.call_args.kwargs["json"]["consulta"]["pergunta"], "Pergunta")
            self.assertEqual(post.call_args.kwargs["timeout"], 35)
        return resultado

    def test_prioriza_mock_sem_expor_contexto_no_corpo(self):
        r = self.chamar({"resposta": MARCADOR, "contexto": CABECALHO + "Regra literal.", "fontes": [FONTE]})
        self.assertEqual(r["resposta"], MARCADOR)
        self.assertEqual(r["fontes"], [{"documento": "norma.pdf (pág. 2)", "trecho": "Regra literal."}])

    def test_preserva_linhas_do_trecho(self):
        self.assertEqual(extrair_trechos(CABECALHO + "Linha 1\nLinha 2", [FONTE]), ["Linha 1\nLinha 2"])

    def test_fontes_repetidas_na_mesma_pagina(self):
        contexto = CABECALHO + "Primeiro" + "\n\n---\n\n" + CABECALHO + "Segundo"
        self.assertEqual(extrair_trechos(contexto, [FONTE, FONTE]), ["Primeiro", "Segundo"])

    def test_nao_inventa_trecho_sem_cabecalho(self):
        self.assertEqual(extrair_trechos("Texto sem associação verificável", [FONTE]), [""])

    def test_nao_associa_fonte_divergente(self):
        for campo, valor in [("arquivo", "outro.pdf"), ("pagina", 3), ("curso", "SI")]:
            with self.subTest(campo=campo):
                self.assertEqual(extrair_trechos(CABECALHO + "Regra", [{**FONTE, campo: valor}]), [""])

    def test_contexto_invalido_ou_vazio(self):
        for contexto in [None, "", 12]:
            with self.subTest(contexto=contexto):
                self.assertEqual(extrair_trechos(contexto, [FONTE]), [""])

    def test_sem_fontes(self):
        self.assertEqual(extrair_trechos(CABECALHO + "Regra", []), [])

    def test_fonte_sem_trecho_nao_usa_legenda_como_citacao(self):
        r = self.chamar({"resposta": MARCADOR, "fontes": [FONTE]})
        self.assertEqual(r["fontes"][0]["trecho"], "")

    def test_sem_resposta_nao_apresenta_contexto_como_geracao(self):
        r = self.chamar({"contexto": CABECALHO + "Regra", "fontes": [FONTE]})
        self.assertNotIn("Regra", r["resposta"])
        self.assertIn("não foi recebida uma resposta gerada", r["resposta"])

    def test_fallback_exibe_minuta(self):
        r = self.chamar({"fallback_acionado": True, "setor_sugerido": "SecGrad", "template_email": "Minuta literal"})
        self.assertIn("Minuta literal", r["resposta"])
        self.assertIn("evidências suficientes", r["resposta"])

    def test_erro_http_permanece_visivel(self):
        r = self.chamar({}, status=503)
        self.assertFalse(r["sucesso"])
        self.assertIn("503", r["erro"])

    def test_erro_de_conexao(self):
        with patch("src.ui.api_client.requests.post", side_effect=ConnectionError("conexão interrompida")):
            r = enviar_pergunta("P", "CC", "novo")
        self.assertFalse(r["sucesso"])
        self.assertIn("conexão interrompida", r["erro"])


if __name__ == "__main__":
    unittest.main()
