# eeprom-proj
## Easy cp2112 EEPROM programmer

Hi. I released the project into Beta. I would be happy if you would use it. This is a program that turns a CP2112 based board like - https://aliexpress.ru/item/32817467990.html?spm=a2g0o.search.list.0.608d746ck2p6pg
Into a programmer for the eeprom of the 24C chips.
With this program you can erase, read content and program the chip. The program works under ubuntu. To set it up you need to install the following packages:

sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt install -y python3-venv
sudo apt install i2c-tools
sudo pip3 install PyQt5
sudo pip install smbus

Use sudo python3 main.py to run the command, because to work with i2c you need to run commands from sudo

If you have a question then email me at sdivcom@yandex.ru and I will be happy to answer you quickly
