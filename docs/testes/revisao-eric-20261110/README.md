# Revisão da contribuição de Eric - 10/11/2026

Commit conferido na main: cd583e4491552f404444d76723853693c00cd398.
O título menciona benchmark e terceira refatoração do ai-service, mas o diff
contém somente package-lock do backend, fallback.config.ts e api_client.py.
Não há alteração do ai-service, novos testes ou evidências antes/depois neste
commit. Não é possível contar o terceiro item apenas pelo título.

## Resultados observados

- A UI passa a priorizar resposta em vez de contexto. Uma chamada HTTP substituída
por mock confirmou o retorno do aviso explícito de simulação. Isso não é um
ensaio no navegador ou um benchmark de respostas reais.
- A legenda de fonte continua sendo `Página N do documento X`, não trecho literal.
- O padrão do fallback mudou de 0,8 para 0,5, sem benchmark anexado ao commit.
- A suíte corrente do backend executou 256 testes: 254 aprovados e duas falhas.
Ambas exigem 0,8 quando a variável não está definida; ver resumo.json.
- E2e que definem 0,8 explicitamente e o ensaio histórico de serviços reais não
validam o novo padrão automaticamente. Não confundir resultados anteriores com
aprovação desta mudança.
- O caso de carburador medido anteriormente em aproximadamente 0,454 é inferior
a ambos os limiares. Reduzir para 0,5 não garante corrigir esse tipo de falso
positivo. A distância precisa ser medida novamente no benchmark atual.

## Decisão nesta revisão

Código de produção, testes e PDFs anteriores não foram alterados. Mantivemos o
resultado com falha, sem mudar asserções para produzir aprovação artificial.
Não há necessidade de reingerir: o corpus não mudou neste commit.

A equipe precisa confirmar se o novo limiar é uma decisão baseada em evidências.
Se provisório para experiência, usar FALLBACK_DISTANCE_THRESHOLD=0.5 no ambiente
de benchmark e preservar o padrão acordado. Se for adotado como novo contrato,
publicar a justificativa e atualizar documentação e testes correntes de forma
coerente, preservando V1/V2 históricas. A calibração é mudança funcional, não
refatoração sem mudança de comportamento.

Eric deve publicar benchmark (perguntas, curso/perfil, fontes e resultado esperado,
resultado observado, distâncias, modo de geração, versão do corpus/código e
limitações), além do ID/commit da terceira refatoração e V2 antes/depois. Se esse
material existir apenas localmente, enviar ao repositório ou compartilhar o pacote
original. Não reconstruir evidências históricas como se tivessem sido executadas.

Rafael poderá então consolidar o terceiro item no PDF de até três páginas,
atualizar a análise crítica e repetir a integração afetada. A pendência EC22 e a
curadoria de Ricardo continuam separadas.

## Reprodução

Em backend/, Node.js 24 e dependências instaladas:

```powershell
node node_modules/vitest/vitest.mjs run
```

backend-unitarios.json e backend-unitarios.txt registram esta execução.
cliente-ui-controlado.json registra a chamada substituída de UI; não é teste visual.
A branch local de revisão é test/revisao-eric-sprint3. Sem commit ou push automático.
