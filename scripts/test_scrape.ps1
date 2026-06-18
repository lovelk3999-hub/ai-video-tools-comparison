$tools = @{
    "HeyGen" = "https://www.heygen.com/pricing"
    "Synthesia" = "https://www.synthesia.io/pricing"
    "Runway" = "https://runwayml.com/pricing"
    "Pika" = "https://pika.art/pricing"
    "Kling" = "https://kling.kuaishou.com"
}

foreach ($t in $tools.Keys) {
    $url = $tools[$t]
    Write-Host "=== $t ($url) ===" -ForegroundColor Cyan
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 15 -ErrorAction Stop
        Write-Host "  Status: $($resp.StatusCode)" -ForegroundColor Green
        Write-Host "  Content-Length: $($resp.Content.Length)"
        
        $content = $resp.Content
        $hasPricing = $content -match '(?i)(price|pricing|\$\d+|free|plan|month|pro|enterprise|creator)'
        Write-Host "  Has pricing keywords: $hasPricing"
        
        if ($content.Length -lt 50000) {
            Write-Host "  [$t] Short content — likely SPA/JS-rendered" -ForegroundColor Yellow
        } else {
            Write-Host "  [$t] Long content — likely SSR, data may be in HTML" -ForegroundColor Green
        }
        
        $scriptCount = ([regex]::Matches($content, '<script')).Count
        Write-Host "  Script tags: $scriptCount"
    }
    catch {
        Write-Host "  ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    Write-Host ""
}
