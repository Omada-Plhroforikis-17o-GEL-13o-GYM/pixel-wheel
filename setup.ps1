# Change directory to 'src'
Set-Location src

# Remove the 'tleng2' directory if it exists
if (Test-Path -Path "tleng2") {
    Remove-Item -Recurse -Force "tleng2"
}

# Clone the game engine into 'src/tleng2'
git clone https://github.com/tl-ecosystem/tleng.git tleng-temp

# Move the nested tleng2 folder to the correct location
Move-Item -Path "tleng-temp/src/tleng2" -Destination "tleng2"

# Clean up the temporary repo
Remove-Item -Recurse -Force "tleng-temp"