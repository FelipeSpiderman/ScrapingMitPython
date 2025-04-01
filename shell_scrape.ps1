#Scraping von Google (statisches HTML)
param (
    [string]$query = "10 most beautiful places in the world"
)
$encodedQuery = [uri]::EscapeDataString($query)
$uri = "https://www.google.com/search?q=$encodedQuery"
Write-Host "Sende Anfrage an: $uri"

try {
    $response = Invoke-WebRequest -Uri $uri
    Write-Host "Anfrage erfolgreich, Statuscode: " $response.StatusCode

    $results = $response.ParsedHtml.getElementsByClassName("Ww4FFb")
    Write-Host "Gefundene Ergebnisse: " $results.Length

    if ($results.Length -eq 0) {
        Write-Host "Keine Ergebnisse gefunden. Google verwendet dynamisches JavaScript, das PowerShell nicht rendern kann."
    } else {
        foreach ($result in $results) {
            try {
                $title = $result.getElementsByTagName("h3")[0].innerText
                Write-Host "Titel: $title"
            } catch {
                Write-Host "Kein Titel gefunden in diesem Ergebnis."
            }
        }
    }
} catch {
    Write-Host "Fehler beim Abrufen der Seite: $_"
}