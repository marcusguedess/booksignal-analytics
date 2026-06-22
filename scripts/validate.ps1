param(
    [string]$BasePath = "",
    [string]$SiteUrl = "http://localhost:3000"
)

$ErrorActionPreference = "Stop"

python analytics/export_booksignal.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m py_compile analytics\export_booksignal.py datasets\booksignal\analysis.py datasets\booksignal\data_loader.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m unittest discover -s tests -p "test_*.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Push-Location web
try {
    npm run lint
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    npm run typecheck
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $env:NEXT_PUBLIC_BASE_PATH = $BasePath
    $env:NEXT_PUBLIC_SITE_URL = $SiteUrl
    npm run build
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
finally {
    Pop-Location
}
