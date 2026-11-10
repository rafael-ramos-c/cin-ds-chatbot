"""Normalização conservadora de páginas com extração vertical de palavras."""
import re


def normalizar_texto_pdf(texto: str) -> str:
    """Recompõe espaços apenas quando predomina o padrão uma palavra por linha.

    Não altera palavras nem tenta interpretar tabelas. Páginas convencionais
    permanecem intactas; parágrafos vazios e marcadores de itens são preservados.
    """
    linhas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
    if len(linhas) < 20:
        return texto
    curtas = sum(len(linha.split()) <= 2 for linha in linhas)
    if curtas / len(linhas) < 0.8:
        return texto
    paragrafos = []
    for bloco in re.split(r"\n\s*\n", texto.replace("\r\n", "\n")):
        # O extrator pode separar inclusive 'Art.' e o número do artigo.
        recomposto = re.sub(r"\s+", " ", bloco).strip()
        recomposto = re.sub(r" (?=(?:Art\.\s*\d+|[IVXLCDM]+\s*[-–]|[•●]))", "\n", recomposto)
        if recomposto:
            paragrafos.append(recomposto)
    return "\n\n".join(paragrafos)
