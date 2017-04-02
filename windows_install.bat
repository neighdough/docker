cd c:\
mkdir docker
cd .\docker
git clone https://github.com/neighdough/docker.git
Invoke-WebRequest -Uri https://download.docker.com/win/stable/InstallDocker.msi -OutFile .\InstallDocker.msi
msiexec /a InstallDocker.msi /quiet
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
shutdown /r
cd docker
docker build -t neighdough/spark .



