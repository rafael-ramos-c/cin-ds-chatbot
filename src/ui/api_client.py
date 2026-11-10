import requests

NESTJS_API_URL = "http://localhost:3000/api/v1/conversa"

def enviar_pergunta(prompt: str, curso: str, perfil: str):
    """
    Envia a pergunta para o NestJS e processa a resposta de contexto
    ou o template de e-mail gerado pelo FallbackService.
    """
    payload = {
        "consulta": {
            "pergunta": str(prompt).strip(),
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
                    ctx = data.get("contexto", "")
                    texto_final = ctx.strip() if ctx.strip() else "Consulta concluída, mas nenhum texto relevante foi extraído dos documentos."
            
            # 3. Tratamento das fontes
            fontes_brutas = data.get("fontes") or []
            fontes_formatadas = []
            for item in fontes_brutas:
                arquivo = item.get("arquivo", "Documento Oficial")
                pagina = item.get("pagina", 1)
                fontes_formatadas.append({
                    "documento": f"{arquivo} (pág. {pagina})",
                    "trecho": f"Página {pagina} do documento {arquivo}"
                })
            
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