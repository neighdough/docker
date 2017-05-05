# Description

This project contains all of the code necessary to deploy and run PySpark using
Docker on a Windows machine. The process for deploying and then running the 
container are as follows:

1. Copy windows_install.bat to remote machine then execute
```bat
net use x: \\computer-name\C$ /user:domain\username
copy-item C:\docker\windows_install.bat x:\windows_install.bat
psexec \\remote-machine c:\windows_install.bat
```
2. Remote machine will restart, login then batch file to build container should
    start automatically
3. Start spark master
```console
/spark_home_directory/sbin/start-master.sh
```
4. Run docker container on remote machine
```console
docker run -P --net=host --add-host=moby:127.0.0.1 -it neighdough/spark ./sbin/start-slave.sh spark://<host-name>:7077
docker run -P --net=host --add-host=moby:127.0.0.1 -it neighdough/spark /bin/bash
```


# Sample Commands

### Run container, mount drive, run interactive
```console
docker run -v /home/nate/dropbox/Classes/FundDataScience_COMP8150/assignments/hw4:/data -it neighdough/spark /bin/bash
```
### In container, specify ipython as pyspark driver
```console
PYSPARK_DRIVER_PYTHON=ipython ./bin/pyspark
```
### Run container, publish all ports
```console
docker run -P --net=host --add-host=moby:127.0.0.1 -it neighdough/spark /bin/bash
```
# Sample pyspark commands

```python
text = sc.textFile('/data/data/sample-text.txt').map(
            lambda line: re.sub(exp, '', line).split(' ')
            ).zipWithIndex()

text.flatMap(lambda x: [[i, x[1]] for i in x[0]]).collect()
```
