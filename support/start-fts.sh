#!/bin/bash

echo "###########################"
echo "Preparing"
echo "###########################"

#Touch
#Create log folders
echo "Create logs folder"
mkdir -p /data/logs/supervisor
mkdir -p /data/database/
mkdir -p /data/certs/ClientPackages/
mkdir -p /data/ExCheck/checklist/
echo "Set permissions on data folder"
chmod -R 777 /data

echo "###########################"
echo "Preparations completed"
echo "###########################"

supervisord -c /etc/supervisor/conf.d/supervisord.conf
