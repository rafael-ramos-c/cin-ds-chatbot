import unittest
from unittest.mock import Mock, patch
from src.ui.conversation import contextualizar
from src.ui.api_client import enviar_pergunta


class ConversationTest(unittest.TestCase):
    def test_continuacao_resolve_segunda_chamada(self):
        q, a = contextualizar('Onde consigo esse requerimento?', [{'role': 'user', 'content': 'Como solicito segunda chamada?'}])
        self.assertIn('segunda chamada de prova', q)
        self.assertFalse(a)

    def test_sem_referente_pede_esclarecimento_sem_http(self):
        with patch('src.ui.api_client.requests.post') as post:
            r = enviar_pergunta('Onde consigo esse requerimento?', 'IA', 'novo')
        post.assert_not_called()
        self.assertIn('A qual', r['resposta'])

    def test_mudanca_assunto_nao_reutiliza_segunda_chamada(self):
        h = [{'role': 'user', 'content': 'Segunda chamada?'}, {'role': 'user', 'content': 'Como faço estágio?'}]
        self.assertTrue(contextualizar('Onde consigo esse requerimento?', h)[1])

    def test_pergunta_completa_inalterada(self):
        q = 'Onde obtenho o requerimento de segunda chamada?'
        self.assertEqual(contextualizar(q, []), (q, False))

    def test_endereco_ausente_nao_repete_procedimento(self):
        data = {'resposta': '[SIMULAÇÃO]', 'contexto': '[Documento: regras.txt | Pág. 1 | Curso: IA]\nPreencha o requerimento.',
                'fontes': [{'arquivo': 'regras.txt', 'pagina': 1, 'curso': 'IA'}]}
        response = Mock(status_code=201)
        response.json.return_value = data
        with patch('src.ui.api_client.requests.post', return_value=response) as post:
            r = enviar_pergunta('Onde consigo esse requerimento?', 'IA', 'novo',
                [{'role': 'user', 'content': 'Como solicito segunda chamada?'}])
        self.assertIn('segunda chamada', post.call_args.kwargs['json']['consulta']['pergunta'])
        self.assertIn('Não encontrei um endereço', r['resposta'])
        self.assertNotIn('https://', r['resposta'])

    def test_erro_tecnico_nao_vira_ausencia_documental(self):
        with patch('src.ui.api_client.requests.post', return_value=Mock(status_code=503, text='indisponível')):
            r = enviar_pergunta('Onde obtenho o requerimento de segunda chamada?', 'IA', 'novo')
        self.assertFalse(r['sucesso'])
