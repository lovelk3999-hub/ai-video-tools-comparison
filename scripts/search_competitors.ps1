$headers = @{"User-Agent"="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
$queries = @(
    "https://www.google.com/search?q=AI+video+tool+pricing+comparison&hl=en",
    "https://www.google.com/search?q=heygen+vs+synthesia+vs+runway+pricing+comparison+2026&hl=en",
    "https://www.google.com/search?q=AI+video+generation+platform+pricing+compare&hl=en",
    "https://www.google.com/search?q=best+AI+video+tool+comparison+site+2026&hl=en"
)

foreach ($q in $queries) {
    Write-Host "`n=== Query: $(([uri]$q).Query) ===" -ForegroundColor Cyan
    try {
        $resp = Invoke-WebRequest -Uri $q -UseBasicParsing -TimeoutSec 10 -Headers $headers -ErrorAction Stop
        # 提取搜索结果标题+链接
        $content = $resp.Content
        $matches = [regex]::Matches($content, '(?i)<h3[^>]*>(.+?)</h3>')
        foreach ($m in $matches | Select-Object -First 8) {
            $title = [regex]::Replace($m.Groups[1].Value, '<[^>]+>', '')
            Write-Host "  $title" -ForegroundColor White
        }
    } catch {
        Write-Host "  Error: $_"
    }
}
