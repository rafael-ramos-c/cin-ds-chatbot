import re

import requests
from src.ui.conversation import contextualizar, pedido_endereco

NESTJS_API_URL = "http://localhost:3000/api/v1/conversa"


def extrair_trechos(contexto, fontes):
    """Associa texto literal às fontes, sem inventar citação para formato desconhecido."""
    if not isinstance(contexto, str):
        return [""] * len(fontes)
    padrao = re.compile(
        r"(?:\A|\n\n---\n\n)\[Documento: (.*?) \| Pág\. (\d+) \| Curso: (.*?)\]\n"
    )
    cabecalhos = list(padrao.finditer(contexto))
    trechos = []
    for indice, fonte in enumerate(fontes):
        if indice >= len(cabecalhos):
            trechos.append("")
            continue
        atual = cabecalhos[indice]
        arquivo, pagina, curso = atual.groups()
        if (arquivo != fonte.get("arquivo") or int(pagina) != fonte.get("pagina")
                or curso != fonte.get("curso")):
            trechos.append("")
            continue
        fim = cabecalhos[indice + 1].start() if indice + 1 < len(cabecalhos) else len(contexto)
        trechos.append(contexto[atual.end():fim].strip())
    return trechos

def enviar_pergunta(prompt: str, curso: str, perfil: str, historico=None):
    """
    Envia a pergunta para o NestJS e processa a resposta de contexto
    ou o template de e-mail gerado pelo FallbackService.
    """
    consulta, ambiguo = contextualizar(str(prompt).strip(), historico or [])
    if ambiguo:
        return {'sucesso': True, 'resposta': 'A qual requerimento ou formulário você se refere? Informe o procedimento, por exemplo, segunda chamada de prova.', 'fontes': []}
    payload = {
        "consulta": {
            "pergunta": consulta,
            "curso": str(curso).strip() if curso else "Geral",
            "perfil": str(perfil).strip() if perfil else "Todos",
            "top_k": 3
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(NESTJS_API_URL, json=payload, headers=headers, timeout=35)
        if response.status_code in (200, 201):
            data = response.json()
            
            # 1. Se o fallback foi ativado no NestJS
            if data.get("fallback_acionado") is True:
                setor = data.get("setor_sugerido", "SecGrad")
                template = data.get("template_email", "Não foi possível gerar o modelo de e-mail.")
                
                texto_final = (
                    f"⚠️ **Não foram encontrados documentos com evidências suficientes para responder com precisão.**\n\n"
                    f"**Setor Recomendado:** `{setor}`\n\n"
                    f"Podes utilizar o modelo abaixo para entrar em contacto com a secretaria:\n\n"
                    f"```text\n{template}\n```"
                )
            else:
                # 2. PRIORIDADE À RESPOSTA GERADA (com o aviso de simulação), usando o contexto apenas como fallback
                resposta_gerada = data.get("resposta")
                if resposta_gerada:
                    texto_final = str(resposta_gerada).strip()
                else:
                    texto_final = "Consulta documental concluída. Consulte as fontes abaixo; não foi recebida uma resposta gerada."
            
            # 3. Tratamento das fontes
            fontes_brutas = data.get("fontes") or []
            trechos = extrair_trechos(data.get("contexto", ""), fontes_brutas)
            fontes_formatadas = []
            for item, trecho in zip(fontes_brutas, trechos):
                arquivo = item.get("arquivo", "Documento Oficial")
                pagina = item.get("pagina", 1)
                fontes_formatadas.append({
                    "documento": f"{arquivo} (pág. {pagina})",
                    "trecho": trecho,
                })

            if (data.get('fallback_acionado') is not True and pedido_endereco(consulta)
                    and not re.search(r'https?://\S+', '\n'.join(trechos), re.I)):
                texto_final = (
                    'Não encontrei um endereço para obter esse requerimento nos trechos consultados. '
                    'A referência ao formulário, sozinha, não informa onde baixá-lo. '
                    'Confirme o endereço com a secretaria ou coordenação do curso. '
                    'Os trechos abaixo são referências da busca, não um link de download.\n\n'
                    '[VERIFICAÇÃO DOCUMENTAL LIMITADA — SEM GERAÇÃO POR LLM]'
                )
            
            return {
                "sucesso": True,
                "resposta": texto_final,
                "fontes": fontes_formatadas
            }
        else:
            return {
                "sucesso": False,
                "erro": f"Erro HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "sucesso": False,
            "erro": f"Falha de ligação ao servidor backend: {str(e)}"
        }
