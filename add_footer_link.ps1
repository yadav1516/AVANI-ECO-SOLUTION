$rootPath = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$files = Get-ChildItem -Path $rootPath -Filter "*.html" -Recurse

foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        
        # We look for the Solar EPC list item to place Residential Solar before it.
        # Check if Solar EPC exists AND Residential Solar is NOT already there.
        if ($content.Contains('href="solar-epc.html">Solar EPC Services</a></li>') -and -not $content.Contains('href="residential.html">Residential Solar</a></li>')) {
            
            # Use regex to capture the indentation (leading spaces) of the line
            # This ensures we match the indentation of the existing list item
            $pattern = '([ \t]*)<li><a href="solar-epc.html">Solar EPC Services</a></li>'
            
            # The replacement will use the captured indentation ($1) for the new line
            # Then adds the new Residential line
            # Then adds a newline character (assuming Windows CRLF)
            # Then repeats the existing match ($0) to keep the original line
            # Note: We use double quotes for `r`n interpretation
            $replacement = '$1<li><a href="residential.html">Residential Solar</a></li>' + "`r`n" + '$0'
            
            $newContent = $content -replace $pattern, $replacement
            
            if ($newContent -ne $content) {
                [System.IO.File]::WriteAllText($file.FullName, $newContent)
                Write-Host "Updated: $($file.Name)"
            } else {
                Write-Host "No match found (regex mismatch): $($file.Name)"
            }
        } else {
            Write-Host "Skipped (Already exists or missing anchor): $($file.Name)"
        }
    } catch {
        Write-Host "Error processing $($file.Name): $_"
    }
}
