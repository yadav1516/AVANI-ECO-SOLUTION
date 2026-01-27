$root = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$files = Get-ChildItem -Path $root -Filter *.html -Recurse

# Mappings: Old Link -> New Link
$replacements = @{
    "https://www.facebook.com/profile.php?id=61563198731468" = "https://www.facebook.com/share/1EB4KJBTuP/";
    "https://www.instagram.com/pareesan_services/" = "https://www.instagram.com/avani_solar?igsh=d3BpczV1bWJ4dXN6";
    "https://www.linkedin.com/company/pareesan-service-pvt-ltd/" = "https://www.linkedin.com/in/avani-eco-solutions-pvt-ltd-354b99352?utm_source=share_via&utm_content=profile&utm_medium=member_android"
}

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        foreach ($key in $replacements.Keys) {
            # Simple string replacement since these are exact URLs
            # Using Replace method of string, which is case-sensitive by default in .NET but usually fine for URLs. 
            # If case-insensitive needed: $content = $content -replace [regex]::Escape($key), $replacements[$key]
            $content = $content.Replace($key, $replacements[$key])
        }

        if ($content -ne $originalContent) {
            [System.IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
            Write-Host "Updated: $($file.Name)"
        }
    } catch {
        Write-Host "Error processing $($file.Name): $_"
    }
}
