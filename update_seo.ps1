
$files = Get-ChildItem -Path . -Filter *.html -Recurse

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $basename = $file.BaseName
    
    # Generate Title/Desc
    $titleText = $basename.Replace("-", " ").Replace("_", " ")
    $titleText = (Get-Culture).TextInfo.ToTitleCase($titleText)
    
    if ($basename -eq "index") {
        $title = "Pareesan Services Pvt Ltd - Premier Solar EPC & Technology Solutions"
        $desc = "Pareesan Services: India's leading Solar EPC company. Industrial, Commercial, and Utility-scale solar solutions with advanced technology and safety standards."
    } else {
        $title = "$titleText - Pareesan Services Pvt Ltd"
        $desc = "Learn more about $titleText at Pareesan Services Pvt Ltd. We provide top-tier Solar EPC solutions, ensuring quality, safety, and sustainability across India."
    }
    
    # Regex Patterns (Case Insensitive ?i, Single Line ?s where needed)
    
    # 1. Viewport
    if ($content -notmatch 'name=["'']viewport["'']') {
        $viewportTag = '    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        $content = $content -replace '(?i)(<head>)', "`$1`n$viewportTag"
    }
    
    # 2. Title
    if ($content -match '(?i)(?s)<title>.*?</title>') {
        $content = $content -replace '(?i)(?s)<title>.*?</title>', "<title>$title</title>"
    } else {
        # Add after head if title missing (rare but possible) or after viewport
        $content = $content -replace '(?i)(<head>)', "`$1`n    <title>$title</title>"
    }

    # 3. Description
    $descTag = "<meta name=`"description`" content=`"$desc`">"
    
    # Check if exists
    if ($content -match '(?i)name=["'']description["'']') {
        # Replace
        $content = $content -replace '(?i)<meta\s+name=["'']description["'']\s+content=["''].*?["'']\s*/?>', $descTag
    } else {
        # Add after title
        if ($content -match '(?i)(?s)<title>.*?</title>') {
            $content = $content -replace '(?i)(?s)(<title>.*?</title>)', "`$1`n    $descTag"
        } else {
            $content = $content -replace '(?i)(<head>)', "`$1`n    $descTag"
        }
    }

    Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    Write-Host "Updated $($file.Name)"
}
