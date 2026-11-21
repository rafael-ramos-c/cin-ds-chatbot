"""Contrato de geração usado pelo serviço de conversa."""

import os

from src.generation_contract import GenerationUnavailable
from src.ollama_generation import gerar_com_ollama
from src.openai_generation import gerar_com_openai


def gerar_resposta(pergunta: str, contexto: str) -> str | None:
    if not pergunta.strip():
        raise ValueError("A pergunta não pode estar vazia.")
    if not contexto.strip():
        return None
    modo = os.getenv("SECGRAD_GENERATION_MODE", "disabled")
    if modo == "ollama":
        return gerar_com_ollama(pergunta, contexto)
    if modo == "openai":
        return gerar_com_openai(pergunta, contexto)
    if modo != "mock":
        raise GenerationUnavailable("Serviço de geração indisponível.")
    # Nunca produzir uma resposta acadêmica fictícia como se fosse documental.
    return "[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]"
