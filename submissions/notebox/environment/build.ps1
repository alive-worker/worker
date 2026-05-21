# Build the Trae-ready notebox image on Windows (PowerShell).
#
# Usage:
#   .\build.ps1                       # build image "notebox-trae"
#   .\build.ps1 -Image my-name        # custom image name
#   .\build.ps1 -HttpProxy http://host:port -HttpsProxy http://host:port
#
# Steps: materialise ../repo.zip into ./repo/, then `docker build`.
param(
    [string]$Image     = "notebox-trae",
    [string]$HttpProxy = "",
    [string]$HttpsProxy = ""
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

$zip  = Join-Path $here "..\repo.zip"
$repo = Join-Path $here "repo"

if (-not (Test-Path $zip)) { throw "repo.zip not found at $zip" }

Write-Host "[build] materialising repo/ from $zip"
if (Test-Path $repo) { Remove-Item -Recurse -Force $repo }
Expand-Archive -Path $zip -DestinationPath $repo -Force

$buildArgs = @("build", "-t", $Image)
if ($HttpProxy)  { $buildArgs += @("--build-arg", "HTTP_PROXY=$HttpProxy") }
if ($HttpsProxy) { $buildArgs += @("--build-arg", "HTTPS_PROXY=$HttpsProxy") }
$buildArgs += "."

Write-Host "[build] docker $($buildArgs -join ' ')"
& docker @buildArgs
if ($LASTEXITCODE -ne 0) { throw "docker build failed ($LASTEXITCODE)" }

Write-Host ""
Write-Host "[build] done. Start it with:"
Write-Host "    docker run -d -p 2222:22 --name notebox $Image"
