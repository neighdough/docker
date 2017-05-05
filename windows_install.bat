cd c:\
mkdir docker_setup
cd .\docker_setup
git clone https://github.com/neighdough/docker.git
cd .\docker
Powershell.exe Invoke-WebRequest -Uri https://download.docker.com/win/stable/InstallDocker.msi -OutFile .\docker\InstallDocker.msi
Powershell.exe Start-Process msiexec.exe -Wait -ArgumentList '/i C:\docker_setup\docker\InstallDocker.msi ALLUSERS=2 ARPSYSTEMCOMPONENT=0 /L*V "C:\docker_setup\docker\fail.log" /quiet'
Powershell.exe Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
Powershell.exe Copy-Item .\build_container.bat -Destination 'C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
shutdown /r




