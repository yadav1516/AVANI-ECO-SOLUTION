
$rootPath = "c:\Users\Lenovo\Documents\GitHub\Avani eco solutions\AVANI-ECO-SOLUTION"
$domain = "https://avaniecosolution.com"
$files = Get-ChildItem -Path $rootPath -Filter "*.html" -Recurse

function Get-PageTitle ($filename) {
    $name = $filename -replace ".html", "" -replace "-", " " 
    $name = (Get-Culture).TextInfo.ToTitleCase($name)
    
    if ($name -eq "Index") {
        return "Avani Eco Solutions Pvt. Ltd. | Leading Solar EPC Solutions Provider"
    }
    return "$name - Avani Eco Solutions Pvt. Ltd."
}

function Get-MetaDescription ($filename) {
    $name = $filename -replace ".html", "" -replace "-", " "
    $name = (Get-Culture).TextInfo.ToTitleCase($name)
    
    if ($name -eq "Index") {
        return "Avani Eco Solutions Pvt. Ltd. offers end-to-end Solar EPC solutions for residential, commercial, and industrial clients. Switch to solar today and save."
    }
    if ($name -eq "Residential") {
        return "Switch to zero electricity bills with Avani Eco Solutions. Hassle-free residential solar installation with government subsidy and easy finance."
    }
    return "Learn about $name at Avani Eco Solutions Pvt. Ltd. We provide top-tier solar services including EPC, Installation, and O&M for a sustainable future."
}

foreach ($file in $files) {
    try {
        $content = [System.IO.File]::ReadAllText($file.FullName)
        $originalContent = $content
        
        # 1. Fix "Pvt. Ltd. Pvt Ltd" typo
        $content = $content -replace "Pvt\.? Ltd\.? Pvt\.? Ltd", "Pvt. Ltd."
        
        # 2. Update Title
        $newTitle = Get-PageTitle $file.Name
        if ($content -match "<title>(.*?)</title>") {
            $content = $content -replace "<title>.*?</title>", "<title>$newTitle</title>"
        }
        
        # 3. Update Meta Description
        $newDesc = Get-MetaDescription $file.Name
        if ($content -match '<meta name="description" content="(.*?)">') {
            # Use dot matches newline regex option if needed, but simple replace usually works for single line
            # PowerShell regex replace can be tricky with capturing groups in replacement string if not careful
            # We construct the whole tag to be safe
            $content = $content -replace '<meta name="description" content=".*?">', "<meta name=`"description`" content=`"$newDesc`">"
        }
        
        # 4. Add Keywords (Simple check)
        $keywords = "solar energy, solar epc, solar installation, avani eco solutions, renewable energy, solar power"
        if ($content -notmatch '<meta name="keywords"') {
             $content = $content -replace "</head>", "    <meta name=`"keywords`" content=`"$keywords`">`n</head>"
        }

        if ($content -ne $originalContent) {
            [System.IO.File]::WriteAllText($file.FullName, $content)
            Write-Host "Updated: $($file.Name)"
        }
    } catch {
        Write-Host "Error processing $($file.Name): $_"
    }
}

# Generate Sitemap
Write-Host "Generating Sitemap..."
$sitemapContent = '<?xml version="1.0" encoding="UTF-8"?>' + "`n"
$sitemapContent += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "`n"
$today = (Get-Date).ToString("yyyy-MM-dd")

foreach ($file in $files) {
    $url = "$domain/$($file.Name)"
    $priority = "0.80"
    
    if ($file.Name -eq "index.html") {
        $url = "$domain/"
        $priority = "1.00"
    }
    
    $sitemapContent += "   <url>`n"
    $sitemapContent += "      <loc>$url</loc>`n"
    $sitemapContent += "      <lastmod>$today</lastmod>`n"
    $sitemapContent += "      <priority>$priority</priority>`n"
    $sitemapContent += "   </url>`n"
}

$sitemapContent += '</urlset>'
[System.IO.File]::WriteAllText("$rootPath\sitemap.xml", $sitemapContent)
Write-Host "Sitemap generated."

# Update robots.txt
$robotsContent = "User-agent: *`nAllow: /`n`nSitemap: $domain/sitemap.xml"
[System.IO.File]::WriteAllText("$rootPath\robots.txt", $robotsContent)
Write-Host "robots.txt updated."
