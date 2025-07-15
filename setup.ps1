# Change directory to 'src'
Set-Location src

# Remove the 'tleng2' directory if it exists
if (Test-Path -Path "tleng2") {
    Remove-Item -Recurse -Force "tleng2"
}

# Clone the game engine into 'src/tleng2'
git clone https://github.com/tl-ecosystem/tleng.git tleng2