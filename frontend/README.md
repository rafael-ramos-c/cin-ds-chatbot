# Frontend SecGrad — base React CInCoders

React 18, Vite, Cinnamon, roteamento e autenticação OIDC do template fornecido.

Veja o [guia completo na raiz](../README.md). Para desenvolvimento: `npm ci`, copie `.env.example` para `.env` se não existir e execute `npm run dev`. Endereço: http://localhost:5173/secgrad/.

O cliente `src/services/api.ts` cuida do Bearer e da renovação de sessão. `src/modules/chat/chat.service.ts` valida o envelope da conversa. `src/pages/chat` contém a interface e seus testes. O layout, o login e a proteção de rotas usam a estrutura Cinnamon do template; os exemplos simulados de tarefas/equipe não estão publicados no SecGrad.

`npm test`, `npm run lint`, `npm run build` e `npm run test:cov` validam a revisão atual. O build de produção recebe somente configuração pública (`VITE_API_URL`, `VITE_KEYCLOAK_JSON`, base `/secgrad/`). O Docker usa build args e Nginx; não injeta configuração via substituição de código JavaScript com sed.

Nunca coloque um client_secret no frontend. Login institucional exige configurar o realm/clientes com os responsáveis pelo CIn; as contas locais do Compose não comprovam LDAP.
