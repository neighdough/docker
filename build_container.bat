cd C:\docker_setup\docker
Powershell.exe Start-Process docker.exe -Wait -ArgumentList 'build -t neighdough/spark .'
DEL "C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\build_container.bat"