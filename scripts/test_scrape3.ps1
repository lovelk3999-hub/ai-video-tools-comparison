$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    "Accept-Language" = "en-US,en;q=0.9"
}

# --- Runway ---
Write-Host "=== Runway - Extract Pricing ===" -ForegroundColor Cyan
$resp = Invoke-WebRequest -Uri "https://runwayml.com/pricing" -UseBasicParsing -TimeoutSec 15
$content = $resp.Content
# Look for dollar amounts near plan names
$prices = [regex]::Matches($content, '(?i)(\$\d+[\d,.]*)\s*/?\s*(month|mo|yr|year)')
Write-Host "  Runway pricing mentions:"
$prices | ForEach-Object { Write-Host "    $($_.Value)" }

$plans = [regex]::Matches($content, '(?i)(Free|Starter|Creator|Pro|Enterprise|Ultimate|Basic)\s*[^<]{0,60}')
Write-Host "  Runway plan names found:"
$plans | Select-Object -First 8 | ForEach-Object { Write-Host "    $($_.Value.Trim())" }

# --- Pika ---
Write-Host "=== Pika - Extract Pricing ===" -ForegroundColor Cyan
$resp = Invoke-WebRequest -Uri "https://pika.art/pricing" -UseBasicParsing -TimeoutSec 15
$content = $resp.Content
$prices = [regex]::Matches($content, '(?i)(\$\d+[\d,.]*)\s*/?\s*(month|mo|yr|year)')
Write-Host "  Pika pricing mentions:"
$prices | ForEach-Object { Write-Host "    $($_.Value)" }
$plans = [regex]::Matches($content, '(?i)(Free|Starter|Creator|Pro|Enterprise|Ultimate|Basic)\s*[^<]{0,60}')
Write-Host "  Pika plan names found:"
$plans | Select-Object -First 8 | ForEach-Object { Write-Host "    $($_.Value.Trim())" }

# --- Kling ---
Write-Host "=== Kling (klingai.com) - Extract Pricing ===" -ForegroundColor Cyan
$resp = Invoke-WebRequest -Uri "https://klingai.com" -UseBasicParsing -TimeoutSec 15 -Headers $headers
$content = $resp.Content
$prices = [regex]::Matches($content, '(?i)(\$\d+[\d,.]*|¥\d+[\d,.]*)\s*/?\s*(month|mo|yr|year|月)')
Write-Host "  Kling pricing mentions:"
$prices | ForEach-Object { Write-Host "    $($_.Value)" }
$plans = [regex]::Matches($content, '(?i)(Free|Starter|Basic|Pro|Enterprise|Ultimate|标准|专业|基础|免费|会员)\s*[^<]{0,60}')
Write-Host "  Kling plan names found:"
$plans | Select-Object -First 8 | ForEach-Object { Write-Host "    $($_.Value.Trim())" }
