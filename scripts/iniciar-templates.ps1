[CmdletBinding()]
param([switch]$Ingerir, [switch]$Demo)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker nao encontrado. Instale e abra o Docker Desktop com engine Linux e Compose V2. Veja README.md.'
}
Push-Location $projectRoot
$previousMode = $env:SECGRAD_GENERATION_MODE
$previousTimeout = $env:AI_SERVICE_TIMEOUT_MS
try {
    if (-not (Test-Path -LiteralPath '.env')) { Copy-Item -LiteralPath '.env.example' -Destination '.env' }
    & docker compose version
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose V2 indisponivel.' }
    & docker info --format '{{.ServerVersion}}'
    if ($LASTEXITCODE -ne 0) { throw 'Abra o Docker Desktop e aguarde a engine iniciar.' }
    if ($Demo) {
        $env:SECGRAD_GENERATION_MODE = 'ollama'
        $env:AI_SERVICE_TIMEOUT_MS = '60000'
        try {
            $tags = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5
        } catch {
            throw 'A API local do Ollama nao respondeu. Inicie o Ollama ou execute ollama serve e tente novamente.'
        }
        if ('qwen3:4b' -notin $tags.models.name) {
            throw 'O modelo nao esta instalado. Execute ollama pull qwen3:4b e tente novamente.'
        }
    }
    & docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw 'Configuracao Compose invalida; confira .env.' }
    & docker compose up -d --build --wait ai-service
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar o servico de IA.' }
    if ($Demo) {
        & docker compose exec -T ai-service python -c "import json, os, urllib.request; url = os.environ['SECGRAD_OLLAMA_URL'].rstrip('/') + '/api/tags'; tags = json.load(urllib.request.urlopen(url, timeout=5)); print('Ollama acessivel a partir do servico de IA'); assert any(model['name'] == 'qwen3:4b' for model in tags['models'])"
        if ($LASTEXITCODE -ne 0) { throw 'O servico de IA no Docker nao conseguiu acessar o Qwen no Ollama. Confira SECGRAD_OLLAMA_URL.' }
    }
    if ($Ingerir) {
        & docker compose exec -T ai-service python -m src.validate_catalog
        if ($LASTEXITCODE -ne 0) { throw 'Catalogo invalido.' }
        & docker compose exec -T ai-service python -m src.ingest_batch
        if ($LASTEXITCODE -ne 0) { throw 'Ingestao incompleta; verifique o catalogo e os PDFs.' }
        # A API e a ingestao usam processos diferentes. Reabra o indice na API apos a escrita.
        & docker compose restart ai-service
        if ($LASTEXITCODE -ne 0) { throw 'Nao foi possivel recarregar o indice no servico de IA.' }
    } else { Write-Host 'Na primeira execucao use -Ingerir para criar a base vetorial do Docker.' }
    & docker compose up -d --build --wait --wait-timeout 120
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar os servicos. Consulte docker compose logs.' }
    Write-Host 'Interface: http://localhost:5173/secgrad/ . Usuarios LOCAIS: user/user ou admin/admin.'
} finally {
    $env:SECGRAD_GENERATION_MODE = $previousMode
    $env:AI_SERVICE_TIMEOUT_MS = $previousTimeout
    Pop-Location
}
