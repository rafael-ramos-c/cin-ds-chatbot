import unittest
from src.pdf_text import normalizar_texto_pdf


class PdfTextTest(unittest.TestCase):
    def test_recompoe_palavras_sem_alterar_conteudo(self):
        palavras = ('O estudante pode realizar estágio não obrigatório após cumprir '
                    'os requisitos previstos no regulamento do curso de Ciência da Computação.').split()
        resultado = normalizar_texto_pdf('\n'.join(palavras))
        self.assertEqual(resultado, ' '.join(palavras))

    def test_preserva_pagina_convencional(self):
        texto = '\n'.join(['Uma linha convencional com várias palavras e informações.'] * 25)
        self.assertEqual(normalizar_texto_pdf(texto), texto)

    def test_preserva_paragrafos_e_artigos(self):
        texto = '\n'.join(['palavra'] * 22) + '\n\nArt.\n3.\nRegra\nArt.\n4.\nOutra'
        resultado = normalizar_texto_pdf(texto)
        self.assertIn('\n\nArt. 3. Regra\nArt. 4. Outra', resultado)

    def test_texto_curto_inalterado(self):
        self.assertEqual(normalizar_texto_pdf('A\nB\nC'), 'A\nB\nC')

    def test_vazio(self):
        self.assertEqual(normalizar_texto_pdf(''), '')
