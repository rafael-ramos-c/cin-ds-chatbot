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

    def test_segunda_chamada_de_prova_exclui_regulamento_de_tg(self):
        c = Colecao()
        buscar_contexto('Como solicito segunda chamada de prova?', 'CC', 'novo', collection=c)
        filtro = c.parametros['where']['$and']
        self.assertIn({'documento': {'$ne': 'regulamento_tg.txt'}}, filtro)
        self.assertIn({'curso_cc': True}, filtro)
        self.assertIn({'perfil_novo': True}, filtro)

    def test_segunda_chamada_de_tg_mantem_filtro_por_assunto(self):
        c = Colecao()
        buscar_contexto('Como solicito segunda chamada da avaliação de TG?', 'CC', 'novo', collection=c)
        self.assertEqual(c.parametros['where'], {'$and': [{'curso_cc': True}, {'perfil_novo': True}]})

    def test_quando_posso_estagiar_prioriza_normas_com_criterios(self):
        class ColecaoComNorma(Colecao):
            def query(self, **kwargs):
                self.parametros = kwargs
                return {'documents': [['deve já ter cumprido os requisitos']],
                        'metadatas': [[{'documento': 'norma.pdf', 'pagina': 3}]],
                        'distances': [[0.52]]}

        c = ColecaoComNorma()
        resultado = buscar_contexto('E a partir de quando eu posso fazer estágio?', 'CC', 'novo', collection=c)
        self.assertIn({'tipo_documento': 'norma_estagio'}, c.parametros['where']['$and'])
        self.assertIn('$or', c.parametros['where_document'])
        self.assertIn({'documento': {'$ne': 'estagio_geral.txt'}}, c.parametros['where']['$and'])
        self.assertEqual(resultado['fontes'][0]['arquivo'], 'norma.pdf')
        self.assertEqual(resultado['distancia_minima'], 0.52)

    def test_si_vigente_prioriza_trecho_que_completa_artigo_de_estagio(self):
        class ColecaoComNorma(Colecao):
            def query(self, **kwargs):
                self.parametros = kwargs
                return {'documents': [['alunos que integralizaram']],
                        'metadatas': [[{'documento': 'norma.pdf', 'pagina': 3}]],
                        'distances': [[0.52]]}

        c = ColecaoComNorma()
        buscar_contexto('Quando posso iniciar estágio não obrigatório?', 'SI', 'novo', collection=c)
        termos = c.parametros['where_document']['$or']
        self.assertIn({'$contains': 'integralizaram'}, termos)
        self.assertNotIn({'$contains': 'pré-requisitos'}, termos)
