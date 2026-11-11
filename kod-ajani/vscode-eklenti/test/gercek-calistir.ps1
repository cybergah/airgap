# Eklentiyi gercek VS Code icinde, kullanicinin profiline dokunmadan dener.
# -Eklenti ile kurulu paket klasoru de denenebilir.
param([string]$Eklenti)
$ErrorActionPreference = 'Stop'
$testler = Split-Path -Parent $PSScriptRoot
$denenen = if ($Eklenti) { $Eklenti } else { $testler }
if ($Eklenti) { $env:KOD_AJANI_KURULU_PAKET = '1' } else { Remove-Item Env:KOD_AJANI_KURULU_PAKET -ErrorAction SilentlyContinue }
"kurulu paket kipi: $([bool]$Eklenti)  eklenti: $denenen"
$gecici = Join-Path $env:TEMP ("kod-ajani-vscode-" + [guid]::NewGuid().ToString('N'))
$proje = Join-Path $gecici 'proje'
New-Item -ItemType Directory -Force $proje | Out-Null
[IO.File]::WriteAllText((Join-Path $proje 'a.py'), "x = 1`n")
$env:KOD_AJANI_SONUC = Join-Path $gecici 'sonuc.json'
$env:KOD_AJANI_VERI = Join-Path $gecici 'veri'
foreach ($d in 'ELECTRON_RUN_AS_NODE','CHROME_CRASHPAD_PIPE_NAME','NODE_USE_SYSTEM_CA') { Remove-Item "Env:$d" -ErrorAction SilentlyContinue }
$kod = Join-Path (Split-Path -Parent (Split-Path -Parent (Get-Command code).Source)) 'Code.exe'
$argumanlar = @(
  "--user-data-dir=`"$gecici\kullanici`"", "--extensions-dir=`"$gecici\eklentiler`"",
  '--disable-workspace-trust', '--skip-welcome', '--skip-release-notes', '--disable-updates', '--new-window',
  "--extensionDevelopmentPath=`"$denenen`"", "--extensionTestsPath=`"$testler\test\gercek\index.js`"", "`"$proje`""
)
$p = Start-Process -FilePath $kod -ArgumentList $argumanlar -PassThru -RedirectStandardOutput "$gecici\kod.out" -RedirectStandardError "$gecici\kod.err"
$bitis = (Get-Date).AddSeconds(150)
$sonuc = $null
while ((Get-Date) -lt $bitis) {
  if (Test-Path $env:KOD_AJANI_SONUC) {
    try { $sonuc = Get-Content -Raw -Encoding utf8 $env:KOD_AJANI_SONUC | ConvertFrom-Json } catch { $sonuc = $null }
    if ($sonuc -and $sonuc.bitti) { break }
  }
  Start-Sleep -Milliseconds 500
}
if (Test-Path $env:KOD_AJANI_SONUC) { Get-Content -Raw -Encoding utf8 $env:KOD_AJANI_SONUC } else {
  'sonuc dosyasi olusmadi'
  "--- kod.err"; Get-Content "$gecici\kod.err" -Tail 12 -ErrorAction SilentlyContinue
  "--- kod.out"; Get-Content "$gecici\kod.out" -Tail 12 -ErrorAction SilentlyContinue
  "Code surecleri: $((Get-CimInstance Win32_Process -Filter "Name='Code.exe'" | Where-Object { $_.CommandLine -like "*$gecici*" } | Measure-Object).Count)"
  Get-ChildItem "$gecici\kullanici\logs" -Recurse -File -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'exthost|main|renderer' } | ForEach-Object { "--- $($_.Name)"; Get-Content $_.FullName -Tail 12 }
}
Start-Sleep -Seconds 2
Get-CimInstance Win32_Process -Filter "Name='Code.exe'" | Where-Object { $_.CommandLine -like "*$gecici*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 1
Remove-Item -Recurse -Force $gecici -ErrorAction SilentlyContinue
if ($sonuc -and $sonuc.gecti) { 'GERCEK VS CODE TESTI GECTI'; exit 0 } else { 'GERCEK VS CODE TESTI GECMEDI'; exit 1 }
