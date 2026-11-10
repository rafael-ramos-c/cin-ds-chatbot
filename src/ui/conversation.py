"""Continuações limitadas e explícitas, sem geração de fatos acadêmicos."""
import re
import unicodedata


def normalizar(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto.lower())
                   if not unicodedata.combining(c))


def contextualizar(pergunta, historico):
    """Resolve apenas referências curtas a formulário; sem referente pede clareza."""
    n = normalizar(pergunta)
    referencia = re.search(r'\b(esse|este|desse|deste|isso|ele)\b', n)
    formulario = re.search(r'\b(requerimento|formulario|documento|isso|ele)\b', n)
    if not (referencia and formulario):
        return pergunta, False
    anteriores = [m.get('content', '') for m in historico if m.get('role') == 'user']
    for anterior in reversed(anteriores[-3:]):
        a = normalizar(anterior)
        if 'segunda chamada' in a or '2ª chamada' in a or '2a chamada' in a:
            return pergunta + ' (referente ao requerimento para segunda chamada de prova)', False
        # Não atravessa uma mudança explícita para outro assunto.
        if not re.search(r'\b(esse|este|desse|deste|isso|ele)\b', a):
            break
    return pergunta, True


def pedido_endereco(pergunta):
    n = normalizar(pergunta)
    return bool(re.search(r'\b(onde|link|endereco|baixar|download)\b', n)
                and re.search(r'\b(requerimento|formulario)\b', n))
