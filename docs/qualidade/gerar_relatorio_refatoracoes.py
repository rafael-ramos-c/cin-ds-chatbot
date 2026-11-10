"""Relatório das três refatorações, com histórico e execução corrente distinguidos.

Executar com reportlab instalado. Não executa testes ou modifica produção.
"""
import argparse
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak

HERE = Path(__file__).resolve().parent
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle(name='Texto', fontName='Helvetica', fontSize=10, leading=13.5, spaceAfter=8))
STYLES.add(ParagraphStyle(name='Titulo', fontName='Helvetica-Bold', fontSize=19, leading=23, spaceAfter=12))
STYLES.add(ParagraphStyle(name='Sub', fontName='Helvetica-Bold', fontSize=11.5, leading=15, spaceBefore=7, spaceAfter=6))
STYLES.add(ParagraphStyle(name='Pequeno', fontName='Helvetica', fontSize=8, leading=10.5, spaceAfter=6))
STYLES.add(ParagraphStyle(name='Codigo', fontName='Courier', fontSize=8, leading=11, spaceAfter=8))
REPO = 'https://github.com/rafael-ramos-c/cin-ds-chatbot'


def construir(destino):
    story = []

    def p(text, style='Texto'):
        story.append(Paragraph(escape(text).replace('\n', '<br/>'), STYLES[style]))

    def h(text):
        p(text, 'Sub')

    def link(label, url):
        story.append(Paragraph(f'<link href="{escape(url)}" color="#135b86">{escape(label)}</link>', STYLES['Pequeno']))

    def tabela(rows):
        cells = [[Paragraph(escape(str(c)), STYLES['Pequeno']) for c in row] for row in rows]
        t = Table(cells, colWidths=[204, 132, 132], repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5edf2')),
                              ('GRID', (0, 0), (-1, -1), .35, colors.HexColor('#bdcbd4')),
                              ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                              ('LEFTPADDING', (0, 0), (-1, -1), 7),
                              ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                              ('TOPPADDING', (0, 0), (-1, -1), 5),
                              ('BOTTOMPADDING', (0, 0), (-1, -1), 5)]))
        story.append(t); story.append(Spacer(1, 8))

    p('Relatório de refatorações', 'Titulo')
    p('Chatbot SecGrad | CInCoders | Sprint 3 | Revisão de 10/11/2026', 'Pequeno')
    p('TRÊS ITENS COM EVIDÊNCIAS ANTES E DEPOIS', 'Sub')
    p('Três itens com ID e commits separados. Os dois primeiros preservam a V2 acadêmica histórica; o terceiro usa a V2 de regressão corrente, derivada da evolução de geração, sem substituir a baseline histórica. Testes delimitam a proteção: não certificam precisão semântica de respostas.')
    h('1. BACK-REF-01 | Victor | Duplicação de decisão')
    p('Local: backend/src/orchestration/fallback.service.ts, identificarSetor. Dois ifs adjacentes retornavam SecGrad. A duplicação fragmentava a manutenção do mesmo destino; uma alteração poderia atualizar só parte das palavras-chave. Categoria: Duplicated Code e integridade conceitual, sem atribuir violação de todos os princípios SOLID.')
    p('Escolha: pequena mudança com proteção da V2 e benefício claro de manutenção. Técnica: Consolidate Conditional Expression. Consolidam-se as cinco verificações com OR e um único retorno, preservando ordem, curto-circuito e prioridade dos ramos NEAP, pós-graduação e padrão.')
    p('Antes: if (A) return S; if (B) return S;\nDepois: if (A || B) return S;', 'Codigo')
    p('A e B são condições puras sobre a mesma string. Essa equivalência e a inspeção do diff sustentam a preservação; testes são evidência complementar. Assuntos mistos mantêm regras herdadas, não passam a representar requisitos novos.')
    tabela([['Evidência histórica', 'Antes', 'Depois'],
            ['V2 congelada (4 arquivos)', '105/105', '105/105'],
            ['Linhas - escopo original', '45/45 (100%)', '43/43 (100%)'],
            ['Branches - escopo original', '53/53 (100%)', '51/51 (100%)'],
            ['Linhas - escopo ampliado', '85/90 (94,44%)', '83/88 (94,31%)'],
            ['Branches - escopo ampliado', '108/113 (95,57%)', '106/111 (95,49%)']])
    p('A redução dos denominadores explica a pequena queda percentual ampliada: permanecem cinco linhas e cinco entradas de branch descobertas. Não houve remoção de testes ou perda de cobertura de caminho antes exercitado. Não somar esta execução aos testes atuais.', 'Pequeno')
    link('Commit BACK-REF-01: f7a067f (diff completo antes/depois)', REPO + '/commit/f7a067fb7886d1b68621ca57af42cf051dfe02a1')
    p('Baseline: 9d328dc. Evidências locais: docs/qualidade/BACK-REF-01-evidencias/antes e depois (execucao.json, estado-versao.json); relatório BACK-REF-01-relatorio.md. HTML completo: docs/testes/evidencias-backend/03_REFATORACAO/antes/coverage/index.html e depois/coverage/index.html.', 'Pequeno')

    story.append(PageBreak())
    p('Validação vetorial com mais coesão', 'Titulo')
    h('2. IA-REF-02 | Rafael | Extract Function')
    p('Local: ai-service/src/retriever.py, buscar_contexto. A função valida entradas, acessa coleção, verifica retorno, formata contexto e monta fontes. A integridade das listas/distâncias é uma responsabilidade distinguível. Categorias: Long Method, coesão e SRP; o problema é a mistura de razões de mudança, não apenas contar linhas.')
    p('Escolha: isolar uma responsabilidade já coberta e de baixo risco. Técnica: Extract Function, extraindo _validar_resultado_vetorial. O bloco permanece no mesmo ponto do fluxo, antes da formatação. A nova função é interna e não cria contrato público nem dependência entre testes e detalhe privado.')
    p('Antes: buscar_contexto contém o bloco que compara os tamanhos das listas e percorre as distâncias, rejeitando tipos inválidos e números não finitos. Depois: buscar_contexto chama a função interna que contém literalmente esse bloco. A validação de páginas permanece no lugar original.')
    p('Listas de comprimentos diferentes e distâncias inválidas continuam lançando InvalidSearchResult com as mesmas mensagens. Não se altera política de fallback, cálculo de distância, fonte ou tratamento HTTP. A extração não resolve todas as responsabilidades restantes do retriever.')
    tabela([['Evidência histórica', 'Antes', 'Depois'],
            ['V2 congelada', '21/21', '21/21'],
            ['Linhas', '91/95 (95,79%)', '93/97 (95,88%)'],
            ['Branches', '41/42 (97,62%)', '41/42 (97,62%)'],
            ['Regressões existentes', 'Não repetidas', '18/18']])
    p('A definição e a chamada acrescentam linhas instrumentadas; o aumento percentual de linhas não é ganho de comportamento testado. O branch faltante continua existindo. A mesma V2 foi congelada em 55a852c antes da mudança; hashes nos dois manifestos permitem conferir a identidade da suíte.')
    link('Commit IA-REF-02: 8e2f8f6 (diff completo antes/depois)', REPO + '/commit/8e2f8f6')
    link('Congelamento da V2: 55a852c', REPO + '/commit/55a852c')
    p('Antes: docs/testes/relatorios/us01-controlado/v2/execucao.json e html/index.html. Depois: docs/qualidade/IA-REF-02-evidencias/depois/execucao.json e html/index.html. Registro: IA-REF-02-divida.md e IA-REF-02-relatorio.md.', 'Pequeno')
    h('Histórico não equivale à certificação da main atual')
    p('As duas frentes acima usam medições históricas controladas. Em 07/11, a IA teve 20 regressões e 21 testes V2 aprovados. As seis falhas correntes de URL do backend foram corrigidas em 08/11: suíte corrente 256/256, e2e 34 aprovados mais dois opt-in aprovados, lint/build aprovados. Dez chamadas HTTP com corpus real e geração mock foram verificadas separadamente. Isso não reescreve os números históricos nem certifica UI ou LLM real. Evidências: docs/testes/fechamento-backend-20261108/.')
    p('A ingestão agora avisa sobre páginas sem texto e possui dois testes novos. É correção de observabilidade/contrato de retorno, não terceira refatoração sem mudança de comportamento. Do mesmo modo, alterar URL padrão é mudança funcional e não substitui a terceira entrega.', 'Pequeno')

    story.append(PageBreak())
    p('Origem da API e reflexão crítica', 'Titulo')
    h('3. BACK-REF-03 | Rafael, assumindo fechamento de Eric')
    p('Local: backend/src/ai-service/ai-service.service.ts, getEndpoint. Parsing, política detalhada de origem, construção da rota e tradução de exceção dividiam o mesmo fluxo. Categorias: Long Method relativo ao fluxo e coesão. A extração melhora a separação local de responsabilidades; não resolve todas as razões de mudança da classe.')
    p('Técnica: Extract Function. O predicado origemInvalida(origin, base) recebe literalmente as sete condições OR, na mesma ordem. Leitura de ambiente, parsing, rota e catch ficam em getEndpoint. Mantêm-se protocolos, regex, credenciais, query, fragmento, caminho, mensagem HTTP e curto-circuito. A função é interna, sem nova API pública.')
    p('Antes: getEndpoint contém if com sete condições. Depois: if (origemInvalida(origin, base)). Escolha: mudança pequena em política já protegida por testes de origens inválidas e dos dois endpoints. Não é a adição de timeout descrita por Eric, que já existia, nem a restauração funcional de 0,8.')
    tabela([['Mesma configuração / Node 24.22.1', 'Antes', 'Depois'],
            ['V2 de regressão corrente', '256/256', '256/256'],
            ['Linhas do AiService', '64/64 (100%)', '65/65 (100%)'],
            ['Branches do AiService', '84/84 (100%)', '84/84 (100%)'],
            ['Funções do AiService', '8/10 (80%)', '9/11 (81,81%)']])
    p('A seleção de 52 testes de geração está contida nos 256; não somar os totais. Hashes da suíte e configuração foram conferidos. A função acrescenta uma linha instrumentada e uma função coberta; não representa comportamento novo. A V2 acadêmica histórica de 105 casos permanece preservada e não é apresentada como reexecutada na produção atual.', 'Pequeno')
    link('Congelamento anterior: 2a33101 | evidência antes da alteração', REPO + '/commit/2a33101')
    link('Refatoração isolada: 27d0d9b | diff antes/depois', REPO + '/commit/27d0d9b')
    p('Evidências: BACK-REF-03-evidencias/antes e depois (vitest-results.json, HTML e estado); comparacao.json. Configuração: backend/vitest.back-ref03.config.mts. Diagnóstico: BACK-REF-03-divida.md. Correções funcionais de UI/limiar ficaram no commit 0b334a7.', 'Pequeno')
    h('Reflexão: inspeção, ferramentas e LLM')
    p('Leitura do fluxo com apoio de LLM identificou decisão repetida, integridade vetorial misturada à formatação e política de URL dentro da construção. O histórico não separa autoria de cada achado; não se atribui descoberta exclusiva à pessoa ou à LLM. A inspeção do diff confirmou ordem e mensagens e rejeitou como refatoração a mudança do limiar e novos tratamentos de erro.')
    p('Vitest/V8, coverage.py e lint medem caminhos e problemas locais, mas não diagnosticam SRP nem validam adequação documental. Não houve Sonar ou ferramenta de smells executada. O benchmark real encontrou aceitação indevida de perguntas externas apesar dos testes verdes: dívida QA-01 permanece aberta. EC22 foi justificada como contracapa administrativa, sem apagar a página. Ver docs/testes/fechamento-final-20261110/.')

    def rodape(canvas, doc):
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#4a5c69'))
        canvas.drawString(59, 30, 'Sprint 3 | Três refatorações | 10/11/2026')
        canvas.drawRightString(A4[0] - 59, 30, str(doc.page))

    SimpleDocTemplate(str(destino), pagesize=A4, rightMargin=59, leftMargin=59,
                      topMargin=45, bottomMargin=48,
                      title='Refatorações da Sprint 3 - três itens',
                      author='Equipe CInCoders - consolidação de Rafael').build(
                          story, onFirstPage=rodape, onLaterPages=rodape)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida', type=Path, default=HERE / 'relatorio-refatoracoes-sprint3-final-20261110.pdf')
    args = parser.parse_args()
    if args.saida.exists():
        parser.error('Use uma saída nova; não substituir evidência anterior automaticamente.')
    construir(args.saida)
