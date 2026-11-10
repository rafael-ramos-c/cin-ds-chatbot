import unittest
from src.retriever import buscar_contexto


class Colecao:
    def query(self, **kwargs):
        self.parametros = kwargs
        return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}


class TopicFilterTest(unittest.TestCase):
    def test_estagio_com_e_sem_acento_preserva_curso_perfil(self):
        for pergunta in ('Quando posso fazer estágio?', 'Quando posso fazer estagio?'):
            with self.subTest(pergunta=pergunta):
                c = Colecao()
                buscar_contexto(pergunta, 'CC', 'novo', collection=c)
                self.assertIn('where_document', c.parametros)
                self.assertEqual(c.parametros['where'], {'$and': [{'curso_cc': True}, {'perfil_novo': True}]})
                self.assertEqual(c.parametros['query_texts'], [pergunta])

    def test_outro_assunto_nao_recebe_restricao(self):
        c = Colecao()
        buscar_contexto('Como solicito dispensa?', collection=c)
        self.assertNotIn('where_document', c.parametros)
