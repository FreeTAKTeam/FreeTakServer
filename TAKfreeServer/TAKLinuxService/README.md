# How To install FreeTakServer on Linux #
* clone repository with the following command 
```
git clone https://github.com/Tapawingo/TAKlib.git
```

* install python3 with the following command 

```
sudo apt update && sudo apt install python3
```

* enter the TAKLinuxService directory
```
cd freeTak/TAKLinuxService
```
* run the following command to start the server on port 8087 (standard)
```
sudo python3 beginServerFromLinux.py
```
*  in alternative you can run
```
 python TAKfreeServer/server.py -p 8089
 ```
 if you run FTS without the demon, the process will depend on the console being open.  it's suggested to use the demon, so that you can close the console

## Notice ##
> this has been tested with Ubuntu 18.04.4
