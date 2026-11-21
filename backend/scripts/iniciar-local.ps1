[CmdletBinding()]
param([switch]$VerificarConfiguracao)
$ErrorActionPreference = 'Stop'
$backendRoot = Split-Path $PSScriptRoot -Parent
if (-not (Test-Path -LiteralPath (Join-Path $backendRoot '.env'))) {
    throw 'Crie backend/.env a partir de .env.example. A API agora exige Keycloak e PostgreSQL; veja README.md.'
}
if ($VerificarConfiguracao) { Write-Host 'Arquivo .env encontrado. A validacao completa ocorre ao iniciar a API.'; return }
Push-Location $backendRoot
try {
    & npm.cmd run start:dev
    if ($LASTEXITCODE -ne 0) { throw 'A API nao iniciou. Confira PostgreSQL, Keycloak e as variaveis do ambiente.' }
} finally { Pop-Location }
