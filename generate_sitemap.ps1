$baseUrl = "https://pareesan.com/"
$sitemapPath = "sitemap.xml"
$files = Get-ChildItem -Filter *.html

$xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>'
$urlsetStart = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
$urlsetEnd = '</urlset>'

$sitemapContent = @($xmlHeader, $urlsetStart)

$currentDate = (Get-Date).ToString("yyyy-MM-dd")

foreach ($file in $files) {
    if ($file.Name -like "google*.html" -or $file.Name -like "test*.html") {
        continue
    }

    $priority = "0.80"
    if ($file.Name -eq "index.html") {
        $priority = "1.00"
        $loc = $baseUrl
    } else {
        $loc = $baseUrl + $file.Name
    }

    $urlEntry = @"
   <url>
      <loc>$loc</loc>
      <lastmod>$currentDate</lastmod>
      <priority>$priority</priority>
   </url>
"@
    $sitemapContent += $urlEntry
}

$sitemapContent += $urlsetEnd

$sitemapContent | Set-Content $sitemapPath -Encoding UTF8
Write-Host "Sitemap generated at $sitemapPath with $($files.Count) URLs."
