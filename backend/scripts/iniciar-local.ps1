# Inicializacao de desenvolvimento local; nao altera configuracao de producao.
[CmdletBinding()]
param([switch]$VerificarConfiguracao)

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($env:AI_SERVICE_URL)) {
    $env:AI_SERVICE_URL = 'http://127.0.0.1:8000'
}
if ([string]::IsNullOrWhiteSpace($env:AI_SERVICE_TIMEOUT_MS)) {
    $env:AI_SERVICE_TIMEOUT_MS = '30000'
}

$origem = $env:AI_SERVICE_URL.Trim()
$uri = $null
if (-not [Uri]::TryCreate($origem, [UriKind]::Absolute, [ref]$uri) -or
    $uri.Scheme -notin @('http', 'https') -or
    $uri.UserInfo -or $uri.Query -or $uri.Fragment -or
    $uri.AbsolutePath -ne '/' -or
    $origem -notmatch '^https?://[^/?#\\]+/?$') {
    throw 'AI_SERVICE_URL invalida. Use somente a origem, por exemplo http://127.0.0.1:8000 (sem /api/v1/buscar).'
}
if ($env:AI_SERVICE_TIMEOUT_MS -notmatch '^\d+$' -or
    [double]$env:AI_SERVICE_TIMEOUT_MS -lt 1 -or
    [double]$env:AI_SERVICE_TIMEOUT_MS -gt 2147483647) {
    throw 'AI_SERVICE_TIMEOUT_MS deve ser um inteiro entre 1 e 2147483647.'
}
Write-Host "Busca configurada: $origem; timeout: $env:AI_SERVICE_TIMEOUT_MS ms."
Write-Host 'O FastAPI deve estar rodando em outro terminal. Este comando nao inicia a IA.'
if ($VerificarConfiguracao) { return }
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) {
    throw 'npm.cmd nao encontrado. Instale Node.js 24 e reabra o terminal.'
}
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    & npm.cmd run start:dev
    if ($LASTEXITCODE -ne 0) { throw "O backend encerrou com codigo $LASTEXITCODE." }
} finally {
    Pop-Location
}
