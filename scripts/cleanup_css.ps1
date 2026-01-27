$path = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION\assets\css\style.css"

# Try reading content, handling encoding
try {
    # -Raw reads as single string
    $content = Get-Content -Path $path -Raw
} catch {
    $content = [System.IO.File]::ReadAllText($path)
}

# Find proper end of file before corruption
# Looking for .client-logo-grid and its container media query closing brace
# .client-logo-grid is inside @media (max-width: 768px) { ... }
$marker = ".client-logo-grid"
$idx = $content.LastIndexOf($marker)

if ($idx -ge 0) {
    # Find first } after marker
    $idx1 = $content.IndexOf("}", $idx)
    # Find second } after that (closing media query)
    $idx2 = $content.IndexOf("}", $idx1 + 1)
    
    if ($idx2 -ge 0) {
        $cleanContent = $content.Substring(0, $idx2 + 1)
    } else {
        # Fallback: just cut at first } if structure is different
        $cleanContent = $content.Substring(0, $idx1 + 1)
    }
} else {
    # If marker not found, check for corruption start directly
    $corruptIdx = $content.IndexOf("/ *   L o c a")
    if ($corruptIdx -ge 0) {
        $cleanContent = $content.Substring(0, $corruptIdx)
    } else {
        # Use full content if nothing found
        $cleanContent = $content
    }
}

$newCss = @"

/* =========================================
   FIXES APPENDED BY ASSISTANT 
   ========================================= */

/* 1. Map Layout Fix (Centered, constrained) */
.locations-grid {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 30px;
}

.location-map {
    width: 100%;
    text-align: center;
    max-width: 1200px;
    margin: 0 auto;
}

.india-map {
    width: auto;
    height: auto;
    max-width: 100%;
    display: block;
    margin: 0 auto;
}

/* 2. Process Grid Fix (6 items in one line) */
@media (min-width: 992px) {
    .process-section .process-grid {
        display: grid !important;
        grid-template-columns: repeat(6, 1fr) !important;
        gap: 15px !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    
    .process-section .process-card {
        margin: 0 !important;
        width: 100% !important;
    }
    
    /* Adjust internal elements */
    .process-section .process-img {
        height: 120px;
    }
    
    .process-section h3 {
        font-size: 1rem;
    }
}
"@

$finalContent = $cleanContent + $newCss
[System.IO.File]::WriteAllText($path, $finalContent, [System.Text.Encoding]::UTF8)
Write-Host "Cleaned and updated style.css"
