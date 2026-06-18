# Try accessing blocked ones with proper browser User-Agent
$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    "Accept" = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    "Accept-Language" = "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
}

# Retry Synthesia with browser headers
Write-Host "=== Synthesia (with browser headers) ===" -ForegroundColor Cyan
try {
    $resp = Invoke-WebRequest -Uri "https://www.synthesia.io/pricing" -UseBasicParsing -TimeoutSec 15 -Headers $headers -ErrorAction Stop
    Write-Host "  Status: $($resp.StatusCode), Length: $($resp.Content.Length)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ $($_.Exception.Message)" -ForegroundColor Red
}

# Retry Kling with browser headers
Write-Host "=== Kling (with browser headers) ===" -ForegroundColor Cyan
try {
    $resp = Invoke-WebRequest -Uri "https://kling.kuaishou.com" -UseBasicParsing -TimeoutSec 15 -Headers $headers -ErrorAction Stop
    Write-Host "  Status: $($resp.StatusCode), Length: $($resp.Content.Length)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ $($_.Exception.Message)" -ForegroundColor Red
}

# Try Kling with different URL pattern
Write-Host "=== Kling (klingai.com) ===" -ForegroundColor Cyan
try {
    $resp = Invoke-WebRequest -Uri "https://klingai.com" -UseBasicParsing -TimeoutSec 15 -Headers $headers -ErrorAction Stop
    Write-Host "  Status: $($resp.StatusCode), Length: $($resp.Content.Length)" -ForegroundColor Green
} catch {
    Write-Host "  ❌ $($_.Exception.Message)" -ForegroundColor Red
}

# Try Pika's pricing data - look for JSON
Write-Host "=== HeyGen - check for embedded JSON ===" -ForegroundColor Cyan
$resp = Invoke-WebRequest -Uri "https://www.heygen.com/pricing" -UseBasicParsing -TimeoutSec 15
$content = $resp.Content
# Look for __NEXT_DATA__ or similar
if ($content -match '__NEXT_DATA__.*?type="application/json">(.+?)</script>') {
    Write-Host "  ✅ Has __NEXT_DATA__ (Next.js)" -ForegroundColor Green
    $json = $matches[1]
    Write-Host "  JSON length: $($json.Length)"
} elseif ($content -match '__NUXT__') {
    Write-Host "  ✅ Has __NUXT__ (Nuxt.js)" -ForegroundColor Green
} elseif ($content -match 'window\.__INITIAL_STATE__') {
    Write-Host "  ✅ Has __INITIAL_STATE__" -ForegroundColor Green
} else {
    Write-Host "  ⚠️ No standard SSR JSON found" -ForegroundColor Yellow
}

# Check for pricing in plain text
if ($content -match '(?i)(\$\d+[.\d]*\s*/\s*month|Free\s*plan|Starter|Creator|Pro\s*|Enterprise)') {
    Write-Host "  ✅ Pricing text found in HTML" -ForegroundColor Green
}
