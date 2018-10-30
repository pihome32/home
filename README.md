
# Install
## Raspberry
1. Install raspbian
2. Tinkerforge daemon
  * <code>
  wget http://download.tinkerforge.com/tools/brickd/linux/brickd_linux_latest_armhf.deb
  sudo dpkg -i brickd_linux_latest_armhf.deb
  </code>
  
3. Node red
4. Inluxdb + chronograf
  * (https://blog.blaisot.org/raspi-timeseries-tick-stack.html)


git clone https://github.com/hallard/RadioHead

###Install bsm2385
sudo apt-get install html-xml-utils
mkdir -p bcm2835 && (wget -qO - `curl -sL http://www.airspayce.com/mikem/bcm2835 | hxnormalize -x -e | hxselect -s '\n' -c "div.textblock>p:nth-child(4)>a:nth-child(1)"` | tar xz --strip-components=1 -C bcm2835 )
cd bcm2835
./configure
make
sudo make install
Enable SPI on rasp


https://www.hackster.io/idreams/getting-started-with-lora-fd69d1
