This guide will attempt to get you up and running with FreeTAKServer from a fresh install of Raspberry Pi OS Lite (Buster)

First we need to create a bootable SD Card.

Download the Lite image from https://www.raspberrypi.org/downloads/raspberry-pi-os/

I'm using the Lite version as I dont intend to use the Raspberry Pi with a Display.
From windows I'm using BalenaEtcher to flash the image onto the SDCard.

Once the SD Card is created, boot the RaspberryPi connected to a Screen, keyboard and Ethernet Cable.
login:pi
password:raspberry

Run the following command to allow you to use ssh to control the raspberry pi remotely.
sudo raspi-config

pick option 5, Interfacing options
pick option 2 SSH
pick yes
press "escape"

WARNING: currently you have an insecure password please change it.
run the following command to change the default password
passwd

enter the password raspberry
now enter twice a new secure password

you can now access the raspberry pi from another computer easily, this will make life easier as you can copy paste the commands.

to find out the IP address of your RaspberryPi enter the following command
ifconfig eth0

some text will scroll up the window, look out for where it says inet, the IP address is in the format X.X.X.X

from the other computer you can now use ssh to connect to the raspberry pi.

username: pi
password: as you changed it above (raspberry if you havent changed it, NOT RECOMMENDED)
ip: X.X.X.X from above
port: 22

There are many terminal emulators to assist with this, Mac OS and Linux typically have SSH out of the box,
Windows does too but you need to jump through hurdles to do so.

Putty is a popular Windows ssh Client, I personally use Termius on all my platforms.


OK we are now at the stage where we have a fresh install of Raspberry Pi OS and we can SSH to it.

Next we need to install a few things to get FreeTAKServer working.
From the commandline or ssh terminal enter the following commands.

sudo apt update -y
sudo apt upgrade -y
sudo apt install python3 python3-pip -y    (It may complain that python3 is already installed, this is fine)
sudo apt install libxml2-dev libxslt-dev -y
sudo pip3 install FreeTAKServer
sudo pip3 install pycairo
sudo  python3 -m FreeTAKServer.controllers.Orchestrator -IP X.X.X.X

You are now cooking with Gas.

On ATAK on your device you need to add an ATAK server, using the IP address of the RaspBerryPi.
Under advanced  options use TCP as the connection type and 8087 as the port.