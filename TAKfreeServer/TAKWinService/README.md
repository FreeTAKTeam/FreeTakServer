> To run FreeTakServer you require admin priviliges

# Installing FreeTakServer on Windows step by step
1. download python for windows 
 (current release  here:  https://www.python.org/ftp/python/3.8.2/python-3.8.2.exe)
2. allow python.exe in firewall
3. install pip from here https://bootstrap.pypa.io/get-pip.py
  * navigate to the directory where it is installed
  * run the following 'py get-pip.py'
  * verify installation using pip -V
4. open whichever port (FTS standard is 8087) you will be using for connections in firewall
 > TIP: kill any program already running on whichever port you've decided to use

5. download the release of FTS from https://github.com/Tapawingo/TAKlib/releases
 5.1 unzip and move to a good location (e.g. 
 ```
 C:\Program Files (x86)
 ```
6.   Press WIN+ X to open the  Command MD with admin(advisable to have green text on black background)

7. cd into whichever directory the file is located 
 ```
 cd C:\Program Files (x86)\FreeTakServer\TAKWinService
 ```

7.1. type the following 
```
beginProgramAsService.py install
```
7.2 REQUIRED: be **very** impressed by the incredible Parrot logo and the profound tagline reference. Failure to fullfil this requirement could delete all your friends from Facebook

8. type 
```
beginProgramAsService.py start
```
9. the service will ask for you internet IP  and a port (8087)

# TROUBLESHOOTING

if you have any issues don't hesitate to bring it up as this program is still in development
<br><br>

## ERROR: Could not find a version that satisfies the requirement win32serviceutil
```
cmd > pip install pywin32
```
## Python windows service “Error starting service: The service did not respond to the start or control request in a timely fashion”
attempt to add python to the system path
```
setx /M PATH "%PATH%;'path to your python installation file';C:\Python38\Scripts;'path to your python installation file'\Lib\site-packages\pywin32_system32;'path to your python installation file'\Lib\site-packages\win32
```
>
side note TAKFreeServer_running_as_service.py can be run independently without being run as service 
