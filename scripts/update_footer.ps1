$targetDir = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$files = Get-ChildItem -Path $targetDir -Recurse -Filter "*.html"

$oldPhonePattern = "\+91\s*9873886002"
$newPhone = "+91 76686 82912, +91 92178 50708"

$oldTelLinkPattern = "tel:\+?91[\s-]?9873886002"
$newTelLink = "tel:+917668682912"

$oldEmail = "info@pareesan.com"
$newEmail = "info@avaniecosolution.com"

# PowerShell regex for multi-line: (?s) turns on single-line mode so . matches newline
$oldAddressPattern = "(?s)Unit\s+no\s+401.*?,?[\s\r\n]+Erose\s+garden.*?Haryana\s+121009"
$newAddress = "591, TR 34, Brij Vihar, Lucknow, 226002"

$count = 0

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content

        # Phone Display
        $content = $content -replace $oldPhonePattern, $newPhone
        
        # Tel Link
        $content = $content -replace $oldTelLinkPattern, $newTelLink

        # Email
        $content = $content.Replace($oldEmail, $newEmail)

        # Address
        $content = $content -replace $oldAddressPattern, $newAddress

        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8
            Write-Host "Updated: $($file.Name)"
            $count++
        }
    }
    catch {
        Write-Host "Error updating $($file.Name): $_"
    }
}

Write-Host "Total files updated: $count"
