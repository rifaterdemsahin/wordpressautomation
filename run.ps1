# Define the path to the text file containing the URLs
$linksFilePath = "C:\Users\rifat\Downloads\outputcontract.txt"

# Check if the file exists
if (-Not (Test-Path -Path $linksFilePath)) {
    Write-Host "The file containing links does not exist. Please check the path and try again."
    exit
}

# Read all URLs from the file into an array
$urls = Get-Content -Path $linksFilePath

# Initialize the counter
$counter = 1

# Iterate over each URL and open it in the default web browser
foreach ($url in $urls) {
    # Print the URL and counter to the console for debugging purposes
    Write-Host "Opening URL #${counter}:" $url

    # Delay for 20 seconds before opening the next URL
    Start-Sleep -Seconds 20

    # Open the URL in the default web browser
    Start-Process "msedge" $url

    # Increment the counter
    $counter++
}
