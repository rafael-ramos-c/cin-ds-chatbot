# Entrega final do SecGrad

## Escopo apresentado

O SecGrad responde a dúvidas de graduação a partir das normas do curso e do perfil curricular selecionados. O frontend React/Vite/Cinnamon e o backend NestJS/Prisma seguem os templates CInCoders. O backend valida a sessão do Keycloak local e consulta o serviço Python. O FastAPI recupera trechos do ChromaDB e usa o Qwen3 4B no Ollama para redigir a resposta em português.

O chat mostra arquivo, página e trechos recuperados. Quando o processo não encontra evidência suficiente, oferece um rascunho de contato com a secretaria para o aluno revisar. O rascunho fica na tela. O PostgreSQL atende a infraestrutura do template. O histórico das perguntas fica na sessão da tela.

O deploy desta entrega é uma demonstração local no notebook anfitrião. O Ollama fica no anfitrião e dispensa chave ou créditos de API. A integração de login institucional fica para os stakeholders. O Compose da demo publica as portas no endereço de loopback e usa credenciais de desenvolvimento.

## Roteiro para a apresentação

1. **Problema e proposta, 45 segundos.** Os procedimentos acadêmicos estão distribuídos em páginas e PDFs. As exigências podem variar por curso e perfil. Mostre como o SecGrad aproxima a resposta da fonte que o aluno pode consultar.
2. **Arquitetura, 45 segundos.** Mostre o caminho React → NestJS → FastAPI → ChromaDB e Ollama. Explique onde o Keycloak entra e como os metadados do catálogo filtram as normas.
3. **Deploy e demo, 2 a 3 minutos.** Mostre `docker compose ps` e abra `http://localhost:5173/secgrad/`. Entre com o usuário de demonstração descrito no README. Selecione Ciência da Computação no perfil vigente. Pergunte como solicitar segunda chamada e depois onde encontrar o requerimento. Abra os trechos e mostre a fonte.
4. **Qualidade e limites, 45 segundos.** Mude o curso e mostre que o chat começa uma nova conversa. Use uma pergunta fora de escopo para demonstrar a contingência. Explique que a equipe avaliou perguntas de referência em um notebook e que a secretaria continua sendo a referência para decisões formais.

## Preparação antes de apresentar

- Abra o Docker Desktop e o Ollama. Siga o [README](../README.md) para instalar o modelo e criar o índice na primeira execução. Reingira os documentos após mudanças na base.
- Execute `.\scripts\iniciar-templates.ps1 -Demo` antes de compartilhar a tela. Ensaie uma pergunta para carregar o modelo e confirme a resposta, as fontes e o login no navegador.
- Mantenha o notebook conectado à energia. Use uma sessão do navegador durante o pitch. A primeira pergunta após o carregamento a frio pode demorar mais.
- Se a interface carregar mas a consulta indicar indisponibilidade, confira o servidor local do Ollama. Execute `ollama serve` em outro terminal se ainda não estiver ativo e reenvie a mensagem na interface.
- Se precisar trocar de computador, repita a instalação e a ingestão antes da apresentação. Planeje a primeira execução com internet para baixar imagens, dependências e modelos.

## O que verificar no ensaio

| Área | Cenário | Resultado esperado |
| --- | --- | --- |
| Backend e login | Abrir sem sessão, entrar, sair e voltar ao chat | O chat exige sessão. Sem token, a API retorna 401 |
| IA | Perguntar como solicitar segunda chamada e depois onde obter o formulário | A resposta se apoia nas regras da SecGrad e a continuação fornece a página oficial |
| Dados | Repetir a pergunta sobre início do estágio em CC, EC, SI e IA | A resposta usa as normas do curso e do perfil, com as condições de modalidade ou jornada quando aplicáveis |
| Interface | Alterar curso e perfil, consultar fontes e testar uma pergunta fora do escopo | Histórico reiniciado, perfil único para IA, trechos expansíveis e contingência com rascunho |
| Indisponibilidade | Testar durante o ensaio, com o serviço de IA parado, e restaurá-lo | A interface apresenta o erro, preserva a pergunta no campo e permite reenviar |

Referência da atualização sobre assinatura eletrônica no catálogo. [Requerimentos e Documentos da SecGrad](https://secgrad.cin.ufpe.br/requerimentos-e-documentos).

## Evidências do ensaio local

O ensaio de 23/11/2026 usou uma instalação isolada com volumes novos no Windows, Docker Desktop, 32 GB de RAM e GPU RTX 5070 Laptop. O Compose subiu com as migrações do PostgreSQL e o catálogo processou 21 de 21 documentos.

| Consulta no Edge | Ponto conferido nas fontes |
| --- | --- |
| Como solicito segunda chamada de prova? | Requerimento, documentos comprobatórios, assinatura eletrônica e prazo |
| Onde consigo esse requerimento? | A pergunta de continuação retornou a página oficial da SecGrad |
| A partir de quando posso fazer estágio? — CC | Norma do perfil vigente, requisitos de créditos por jornada |
| A partir de quando posso fazer estágio? — EC | Norma do perfil vigente, percentual de carga horária das disciplinas obrigatórias |
| A partir de quando posso fazer estágio? — SI | Norma do perfil vigente, créditos por jornada e semestre mínimo aplicável |
| A partir de quando posso fazer estágio? — IA | Norma do perfil único, requisitos de créditos por jornada |
| Qual é a receita de bolo de cenoura? | Contingência documental com rascunho de e-mail |

O login local abriu o chat e a saída pelo menu retornou à tela de acesso. A API devolveu HTTP 401 sem sessão. Ao parar o serviço de IA, a API respondeu HTTP 503. O navegador preservou a pergunta no campo e o reenvio funcionou sem duplicação após restaurar o serviço. A interface coube em uma largura de 390 px no fluxo testado.

As suítes passaram com 293 testes do backend, 49 do frontend e 41 de IA. O recorte HTTP da migração reúne 25 dos 293 testes. Os builds do frontend e do backend passaram. O lint do backend teve 24 avisos de estilo em arquivos de teste e nenhum erro.

O ensaio cobre perguntas de referência no perfil vigente ou único e uma sessão por vez. A cobertura de todos os procedimentos, a carga simultânea e o uso institucional ficam fora do resultado medido.
