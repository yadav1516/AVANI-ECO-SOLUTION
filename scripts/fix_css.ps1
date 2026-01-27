$path = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION\assets\css\style.css"
$bytes = [System.IO.File]::ReadAllBytes($path)
# Decode as UTF8 essentially (or try to read strings)
# Using Get-Content -Raw is better but if encoding is mixed, it might fail.

# Let's try reading as text, if it fails, fallback.
try {
    $content = Get-Content -Path $path -Raw
} catch {
    Write-Host "Read failed, trying latin1 or default"
    $content = [System.IO.File]::ReadAllText($path)
}

# Find corruption
$corruptionIndex = $content.IndexOf(". l o c a t i o n s")
if ($corruptionIndex -lt 0) {
    # Try looking for just the spaced check
    $corruptionIndex = $content.IndexOf("/ *   L o c a")
}

if ($corruptionIndex -ge 0) {
    # Find the last closing brace before corruption
    $cutOff = $content.LastIndexOf("}", $corruptionIndex)
    if ($cutOff -ge 0) {
        $cleanContent = $content.Substring(0, $cutOff + 1)
        
        $newCss = @"

/* Locations Map Full Width Update */
.locations-section .container-fluid {
    width: 100%;
    padding: 0;
    max-width: 100%;
}

.locations-grid {
    width: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
}

.location-map {
    width: 100%;
    text-align: center;
}

.india-map {
    width: 100%;
    height: auto;
    max-width: 100%;
    display: block;
    margin: 0 auto;
}
"@
        $finalContent = $cleanContent + $newCss
        [System.IO.File]::WriteAllText($path, $finalContent, [System.Text.Encoding]::UTF8)
        Write-Host "Fixed style.css"
    } else {
        Write-Host "Could not find cut-off point."
    }
} else {
    Write-Host "Corruption pattern not found. Appending anyway?"
    # If not found, maybe it's not spaced?
    # Or maybe it's already fixed?
    # Let's check if the good CSS is there.
    if ($content.Contains("locations-section .container-fluid")) {
        Write-Host "CSS seems present."
    } else {
        Write-Host "Appending CSS..."
        $newCss = @"

/* Locations Map Full Width Update */
.locations-section .container-fluid {
    width: 100%;
    padding: 0;
    max-width: 100%;
}

.locations-grid {
    width: 100%;
    margin: 0;
    display: flex;
    justify-content: center;
}

.location-map {
    width: 100%;
    text-align: center;
}

.india-map {
    width: 100%;
    height: auto;
    max-width: 100%;
    display: block;
    margin: 0 auto;
}
"@
        Add-Content -Path $path -Value $newCss -Encoding UTF8
    }
}
