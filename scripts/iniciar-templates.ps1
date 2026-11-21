[CmdletBinding()]
param([switch]$Ingerir)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Docker nao encontrado. Instale e abra o Docker Desktop com engine Linux e Compose V2. Veja README.md.'
}
Push-Location $projectRoot
try {
    if (-not (Test-Path -LiteralPath '.env')) { Copy-Item -LiteralPath '.env.example' -Destination '.env' }
    & docker compose version
    if ($LASTEXITCODE -ne 0) { throw 'Docker Compose V2 indisponivel.' }
    & docker info --format '{{.ServerVersion}}'
    if ($LASTEXITCODE -ne 0) { throw 'Abra o Docker Desktop e aguarde a engine iniciar.' }
    & docker compose config --quiet
    if ($LASTEXITCODE -ne 0) { throw 'Configuracao Compose invalida; confira .env.' }
    & docker compose up -d --build ai-service
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar o servico de IA.' }
    if ($Ingerir) {
        & docker compose exec -T ai-service python -m src.validate_catalog
        if ($LASTEXITCODE -ne 0) { throw 'Catalogo invalido.' }
        & docker compose exec -T ai-service python -m src.ingest_batch
        if ($LASTEXITCODE -ne 0) { throw 'Ingestao incompleta; verifique o catalogo e os PDFs.' }
    } else { Write-Host 'Na primeira execucao use -Ingerir para criar a base vetorial do Docker.' }
    & docker compose up -d --build
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao iniciar os servicos. Consulte docker compose logs.' }
    Write-Host 'Interface: http://localhost:5173/secgrad/ . Usuarios LOCAIS: user/user ou admin/admin.'
    Write-Host 'Aguarde a inicializacao do Keycloak. LDAP institucional depende de configuracao externa.'
} finally { Pop-Location }
