# Contrato autenticado do SecGrad — migração de 12/11/2026

Rota: `POST /secgrad/api/v1/conversa`. Cabeçalhos: `Content-Type: application/json`, `Authorization: Bearer <access_token>`. O token é do cliente público `secgrad-front`, deve ter audiência `secgrad-back`, issuer do realm configurado e papel reconhecido. O realm local contém o mapeador de audiência do template.

## Entrada

```json
{
  "consulta": {
    "pergunta": "Onde consigo esse requerimento?",
    "curso": "Inteligência Artificial",
    "perfil": "Único Perfil",
    "top_k": 3
  },
  "historico": [
    {"role":"user", "content":"Como solicito segunda chamada?"}
  ]
}
```

`consulta` e `pergunta` são obrigatórios; pergunta até 2000 caracteres úteis. `curso`, `perfil` e `top_k` são opcionais (Geral, Todos e 3 no serviço de domínio). Aceitam-se códigos e rótulos dos quatro cursos, normalizados na entrada. Perfis: novo/vigente/único ou anterior/antigo, além de Todos/ambos. IA não aceita perfil anterior. `top_k` é inteiro de 1 a 10. Campos extras são rejeitados.

`historico` é opcional, com até dez perguntas de até 2000 caracteres. Somente as últimas três são consideradas pelo resolvedor limitado. Não há garantia de compreensão de uma conversa genérica. `dados_email` opcional mantém nome, matrícula, assunto e resumo (strings não vazias até 2000 caracteres cada). Não segue ao serviço de IA nem é armazenado.

## Sucesso

Status 201, envelope do boilerplate:

```json
{
  "statusCode":201,
  "timestamp":"<instante ISO>",
  "path":"/secgrad/api/v1/conversa",
  "data":{
    "resposta":"[SIMULAÇÃO DE INTEGRAÇÃO — NÃO É RESPOSTA ACADÊMICA]",
    "contexto":"<contexto recuperado>",
    "fontes":[{"arquivo":"regras_requerimentos.txt","pagina":1,"curso":"Geral","trecho":"<trecho associado>"}],
    "distancia_minima":0.2,
    "fallback_acionado":false,
    "modo_resposta":"simulacao"
  }
}
```

O exemplo ilustra estrutura, não é evidência de execução nem de resposta acadêmica correta. `modo_resposta` pode ser simulacao, geracao, fallback, esclarecimento ou verificacao_limitada. O nome geracao não certifica precisão; atualmente não há provedor real configurado.

Fallback: `fallback_acionado=true`, `setor_sugerido` e `template_email`, sem resposta acadêmica inventada. Esclarecimento: `esclarecimento_necessario=true`, sem chamada à IA. Pedido de endereço sem URL nos trechos, no modo simulado: mensagem explícita de limitação.

## Erros

Problem Details: `type`, `title`, `status`, `detail`, `instance`, `code`, `timestamp`; erros de validação podem incluir `errors` por campo. Status: 401 identidade ausente/inválida, 403 papel/audiência negados, 422 corpo inválido, 502 resposta externa inválida, 503 indisponibilidade, 504 timeout. Não transformar falha técnica em falta de evidência.

## Separação de contratos

O FastAPI interno conserva `/api/v1/buscar` e `/api/v1/gerar`, sem o envelope NestJS. A URL antiga pública `/api/v1/conversa` não é um alias anônimo na aplicação nova. A interface Streamlit histórica não recebe exceção de autenticação.
