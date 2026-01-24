$textReplacements = @{
    "Pareesan Services Pvt. Ltd." = "Avani Eco Solutions Pvt. Ltd.";
    "Pareesan Services" = "Avani Eco Solutions Pvt. Ltd.";
    "Pareesan" = "Avani Eco Solutions Pvt. Ltd."
}

$logoReplacements = @{
    "assets/img/general/logo_nav.png" = "assets/img/general/avani_logo.png";
    "assets/img/general/logo_transparent.png" = "assets/img/general/avani_logo.png"
}

Get-ChildItem -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $originalContent = $content
    
    foreach ($key in $textReplacements.Keys) {
        $content = $content.Replace($key, $textReplacements[$key])
    }
    
    foreach ($key in $logoReplacements.Keys) {
        $content = $content.Replace($key, $logoReplacements[$key])
    }
    
    if ($content -ne $originalContent) {
        Set-Content -Path $_.FullName -Value $content -Encoding UTF8
        Write-Host "Updated $($_.Name)"
    }
}
