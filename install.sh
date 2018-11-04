#!/bin/sh
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3-pip python-pip 
sudo pip install tinkerforge paho-mqtt
sudo apt-get install mosquitto mosquitto-clients python-mosquitto
sudo apt-get install libusb-1.0-0 libudev0 pm-utils
mkdir /home/pi/tinkerforge 
cd /home/pi/tinkerforge 
wget http://download.tinkerforge.com/tools/brickd/linux/brickd_linux_latest_armhf.deb 
sudo dpkg -i brickd_linux_latest_armhf.deb
rm brickd_linux_latest_armhf.deb 
wget https://raw.githubusercontent.com/Tinkerforge/brick-mqtt-proxy/master/brick-mqtt-proxy.py




sudo apt-get install git-core

git clone https://github.com/pihome32/home.git

sudo echo "deb https://repos.influxdata.com/debian $(grep -e '^VERSION=' /etc/os-release | sed -e 's/^.*(\(.*\)).*$/\1/') stable" > /etc/apt/sources.list.d/influxdb.list
sudo curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
sudo aptitude update

sudo aptitude install influxdb influxdb-client
sudo systemctl enable influxdb
sudo systemctl start influxdb

sudo aptitude install chronograf
sudo systemctl enable chronograf
sudo systemctl start chronograf

cd
git clone git://git.drogon.net/wiringPi
cd ~/wiringPi
git pull origin
./build

cd

pip3 install Pillow
 
sudo apt-get install apt-transport-https curl
curl https://bintray.com/user/downloadSubjectPublicKey?username=bintray | sudo apt-key add -
echo "deb https://dl.bintray.com/fg2it/deb stretch main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install grafana

bash <(curl -sL https://raw.githubusercontent.com/node-red/raspbian-deb-package/master/resources/update-nodejs-and-nodered)