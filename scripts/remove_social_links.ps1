$root = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$files = Get-ChildItem -Path $root -Filter *.html -Recurse

# Twitter
$twitterPattern = '<a\s+href="javascript:void\(0\)"\s+aria-label="Twitter">\s*<i\s+class="fab\s+fa-twitter">\s*</i>\s*</a>'

# YouTube
$youtubePattern = '<a\s+href="https://www\.youtube\.com/@PareesanServices"\s+aria-label="YouTube"\s+target="_blank">\s*<i\s+class="fab\s+fa-youtube">\s*</i>\s*</a>'

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        # Normalize line endings just in case, though usually raw works fine.
        # But regex matching across lines in PS with -Raw handles CRLF.
        
        $originalContent = $content

        # Remove Twitter (Multiline regex)
        $content = [regex]::Replace($content, $twitterPattern, "", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase -bor [System.Text.RegularExpressions.RegexOptions]::Singleline)
        
        # Remove YouTube
        $content = [regex]::Replace($content, $youtubePattern, "", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase -bor [System.Text.RegularExpressions.RegexOptions]::Singleline)

        if ($content -ne $originalContent) {
            # Use NoNewline to prevent extra newlines if raw read includes them effectively
            # Actually standard Set-Content might add one at end. Use [IO.File]::WriteAllText to be precise if needed.
            [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
            Write-Host "Updated: $($file.Name)"
        }
    } catch {
        Write-Host "Error processing $($file.Name): $_"
    }
}
