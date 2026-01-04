$files = Get-ChildItem -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $newContent = $content
    
    $desktopTarget = '<li><a href="catalogue.html" class="nav-link">Catalogue</a></li>'
    $desktopReplacement = '<!-- <li><a href="catalogue.html" class="nav-link">Catalogue</a></li> -->'
    
    $mobileTarget = '<li><a href="catalogue.html">Catalogue</a></li>'
    $mobileReplacement = '<!-- <li><a href="catalogue.html">Catalogue</a></li> -->'
    
    if ($newContent.Contains($desktopTarget)) {
        $newContent = $newContent.Replace($desktopTarget, $desktopReplacement)
    }
    
    if ($newContent.Contains($mobileTarget)) {
        $newContent = $newContent.Replace($mobileTarget, $mobileReplacement)
    }
    
    if ($content -ne $newContent) {
        Set-Content $file.FullName $newContent -Encoding UTF8
        Write-Host "Modified: $($file.Name)"
    }
}
