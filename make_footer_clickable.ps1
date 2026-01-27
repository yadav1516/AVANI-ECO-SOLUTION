
$rootPath = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$files = Get-ChildItem -Path $rootPath -Filter "*.html" -Recurse

foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $originalContent = $content
        
        # Phone 1
        # Search for: <li><i class="fas fa-phone"></i> <strong>Phone:</strong> +91 76686 82912</li>
        # Replace with link
        if ($content -match '\+91 76686 82912' -and $content -notmatch 'href="tel:\+917668682912"') {
            $content = $content -replace '(\+91 76686 82912)', '<a href="tel:+917668682912" style="color: inherit;">$1</a>'
        }

        # Phone 2
        # Search for: +91 92178 50708
        if ($content -match '\+91 92178 50708' -and $content -notmatch 'href="tel:\+919217850708"') {
            $content = $content -replace '(\+91 92178 50708)', '<a href="tel:+919217850708" style="color: inherit;">$1</a>'
        }
        
        # Email
        # info@avaniecosolution.com
        if ($content -match 'info@avaniecosolution.com' -and $content -notmatch 'href="mailto:info@avaniecosolution.com"') {
            $content = $content -replace '(info@avaniecosolution.com)', '<a href="mailto:info@avaniecosolution.com" style="color: inherit;">$1</a>'
        }

        if ($content -ne $originalContent) {
            [System.IO.File]::WriteAllText($file.FullName, $content)
            Write-Host "Updated: $($file.Name)"
        }
    } catch {
        Write-Host "Error processing $($file.Name): $_"
    }
}
