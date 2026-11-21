"""Client for the optional OpenAI Responses API provider."""

import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen


from src.generation_contract import GenerationUnavailable, INSTRUCTIONS, SCHEMA, validar_resposta


def _ler_saida(envelope: dict, contexto: str) -> str | None:
    if envelope["status"] != "completed":
        raise GenerationUnavailable("Serviço de geração indisponível.")
    mensagens = [
        item for item in envelope["output"]
        if item.get("type") == "message" and item.get("role") == "assistant"
    ]
    if len(mensagens) != 1:
        raise ValueError("Resposta do provedor sem uma mensagem única.")
    partes = mensagens[0]["content"]
    if any(parte.get("type") == "refusal" for parte in partes):
        return None
    dados = json.loads("".join(p["text"] for p in partes if p.get("type") == "output_text"))
    return validar_resposta(dados, contexto)


def gerar_com_openai(pergunta: str, contexto: str) -> str | None:
    chave = os.getenv("OPENAI_API_KEY", "").strip()
    modelo = os.getenv("SECGRAD_OPENAI_MODEL", "gpt-5.4-mini").strip()
    if not chave or not modelo:
        raise GenerationUnavailable("Serviço de geração indisponível.")

    dados = {
        "model": modelo,
        "store": False,
        "instructions": INSTRUCTIONS,
        "input": json.dumps({"pergunta": pergunta, "trechos": contexto}, ensure_ascii=False),
        "reasoning": {"effort": "low"},
        "max_output_tokens": 1000,
        "text": {"format": {
            "type": "json_schema", "name": "resposta_secgrad", "strict": True, "schema": SCHEMA,
        }},
    }
    requisicao = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(dados).encode("utf-8"),
        headers={"Authorization": f"Bearer {chave}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(requisicao, timeout=15) as retorno:
            return _ler_saida(json.load(retorno), contexto)
    except (URLError, OSError, ValueError, TypeError, KeyError, AttributeError):
        raise GenerationUnavailable("Serviço de geração indisponível.") from None
