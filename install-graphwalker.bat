mkdir C:\graphwalker
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = 'tls12'; Invoke-WebRequest -Uri 'https://github.com/GraphWalker/graphwalker-project/releases/download/4.3.1/graphwalker-cli-4.3.1.jar' -outfile 'C:\graphwalker\graphwalker-cli-4.3.1.jar'" & :: Downloads GraphWalker CLI using powershell command Invoke-Request

@echo off
@echo @echo off> gw.bat
@echo java -jar C:\graphwalker\graphwalker-cli-4.3.1.jar %*>> gw.bat
@echo on

setx PATH "%PATH%;C:\graphwalker" & :: Adds GraphWalker CLI to the current user PATH
