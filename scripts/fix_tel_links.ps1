$targetDir = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$files = Get-ChildItem -Path $targetDir -Recurse -Filter "*.html"

# The pattern we created by mistake: tel:+91 76686 82912, +91 92178 50708
# We want to revert it to: tel:+917668682912

# Regex to find the messed up tel link
# We need to escape the + and match the spaces/commas
$brokenTelPattern = "tel:\+91\s*76686\s*82912,\s*\+91\s*92178\s*50708"
$fixedTel = "tel:+917668682912"

$count = 0

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content

        $content = $content -replace $brokenTelPattern, $fixedTel

        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8
            Write-Host "Fixed: $($file.Name)"
            $count++
        }
    }
    catch {
        Write-Host "Error fixing $($file.Name): $_"
    }
}

Write-Host "Total files fixed: $count"
