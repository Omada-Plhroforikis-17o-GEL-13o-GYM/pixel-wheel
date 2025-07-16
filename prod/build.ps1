git pull origin main
Remove-Item -Recurse -Force src/tleng2

Set-Location src
Remove-Item -Recurse -Force tleng2
git clone https://github.com/tl-ecosystem/tleng.git tleng-temp
Move-Item tleng-temp/src/tleng2 tleng2
Remove-Item -Recurse -Force tleng-temp
Set-Location ..

python setup.py build