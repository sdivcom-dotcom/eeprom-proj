import smbus
import os
import subprocess
import sys
import time
from itertools import zip_longest
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QFrame, QApplication, QProgressBar, QMessageBox, QTextBrowser, QFileDialog)
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit

command_lsusb = "lsusb | grep 'Silicon Labs CP2112 HID I2C Bridge'"
command_find_i2c_line  = "i2cdetect -l | grep 'CP2112 SMBus Bridge'"
command_find_addr = "i2cdetect -y "
command_find_addr_50 = " | grep '50 -- '"
command_uptime = "cat /proc/uptime"
data_00 = 0x00

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.col = QColor(50, 150, 255)

        b1 = QPushButton('Discover chip', self)
        b2 = QPushButton('Prog chip', self)
        b3 = QPushButton('Erase chip', self)
        b4 = QPushButton('Read chip', self)
        b5 = QPushButton('Verify chip', self)
        b6 = QPushButton('Auto chip', self)
        b7 = QPushButton('Add file', self)

        b1.move(50, 130)
        b2.move(50, 170)
        b3.move(50, 210)
        b4.move(50, 250)
        b5.move(50, 290)
        b6.move(50, 330)
        b7.move(50, 370)

        b1.clicked.connect(self.c1)
        b2.clicked.connect(self.c2)
        b3.clicked.connect(self.c3)
        b4.clicked.connect(self.c4)
        b5.clicked.connect(self.c5)
        b6.clicked.connect(self.c6)
        b7.clicked.connect(self.c7)

        self.nameLabel1 = QLabel(self)
        self.nameLabel1.setText('Model chip:')
        self.line1 = QLineEdit(self)

        self.line1.move(120, 20)
        self.line1.resize(200, 32)
        self.nameLabel1.move(10, 25)

        self.nameLabel2 = QLabel(self)
        self.nameLabel2.setText('Size bytes chip:')
        self.line2 = QLineEdit(self)

        self.line2.move(120, 70)
        self.line2.resize(200, 32)
        self.nameLabel2.move(10, 75)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 410, 200, 32)
        self.pbar.setValue(0)

        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle('CP2112 Eeprom prog 0.1 alfa')
        self.show()

    def lsusb_find(self):
        val = os.system(command_lsusb)
        if val == 0:
            value = 1
        else:
            value = 0
        return value

    # Find i2c line cp2112
    def find_i2c_line(self):
        val = os.system(command_find_i2c_line)
        if val == 0:
            value = subprocess.check_output(command_find_i2c_line, shell=True)
            value = (value[4:6])
        else:
            value = 0
        return value

# Find address chip
    def find_address(self):
        bus_find = self.find_i2c_line()
        bus_find = str(bus_find, encoding="utf-8")
        command_find_address = command_find_addr + bus_find
        os.system(command_find_address)
        val = subprocess.check_output(command_find_address, shell=True)
        value = str(val, encoding="utf-8")

        index1 = value.find("51")
        index2 = value.find("52")
        index3 = value.find("53")

        if index1 >= 10:
            address = 51
            print(address)

        elif index2 >= 10:
            address = 52
            print(address)

        elif index3 >= 10:
            address = 53
            print(address)
        else:
            address = 00
            print(address)
        return address

# Find address chip 0x50
    def find_50_address(self):
        bus_find = self.find_i2c_line()
        bus_find_50 = str(bus_find, encoding="utf-8")
        command_find_50_addr = command_find_addr + bus_find_50 + command_find_addr_50
        val = os.system(command_find_50_addr)
        if val == 0:
            value = subprocess.check_output(command_find_50_addr, shell=True)
            address = 50
        else:
            address = 00
        return address

#audit address
    def count_addr(self):
        value = self.lsusb_find()
        if value == 1:
            val = self.find_address()
            valu = self.find_50_address()
            if val <= 50:
                court = 0
            else:
                court = 1
            if valu <= 49:
                court = 0
            else:
                court = 2
        else:
            print("Chip not found")
        return court


#Discover chip
    def c1(self):
        value = self.lsusb_find()
        if value == 1:
            val = self.find_address()
            valu = self.find_50_address()
            if val <= 50:
                self.pbar.setValue(0)
            else:
                self.pbar.setValue(100)
            if valu <= 49:
                self.pbar.setValue(0)
            else:
                self.pbar.setValue(100)
        else:
            print("Chip not found")
            self.pbar.setValue(0)

#Prog chip
    def c2(self):
        val = self.line2.text()
        res = int(val)
        bus_line = self.find_i2c_line()
        bus_line_int = int(bus_line)
        bus = smbus.SMBus(bus_line_int)
        val = self.count_addr()

        if val == 2:
            bus_addr_int = 0x50
        if val == 1:
            bus_addr = self.find_address()
            bus_addr_int = int(bus_addr)

        H_Byte = 0x00
        L_Byte = 0x00
        print(file)


#Erase chip
    def c3(self):
        val = self.line2.text()
        res = int(val)
        bus_line = self.find_i2c_line()
        bus_line_int = int(bus_line)
        bus = smbus.SMBus(bus_line_int)
        val = self.count_addr()

        if val == 2:
            bus_addr_int = 0x50
        if val == 1:
           bus_addr = self.find_address()
           bus_addr_int = int(bus_addr)

        H_Byte = 0x00
        data_00 = 0x00
        address = 0x00

        for y in range(0, res):
            L_Byte_Data = [address, data_00]
            bus.write_i2c_block_data(bus_addr_int, H_Byte, L_Byte_Data)
            print(address)
            address = address + 1
            time.sleep(0.01)

        print("end")
        self.pbar.setValue(100)

#Read chip
    def c4(self):
        val = self.line2.text()
        res = int(val)
        bus_line = self.find_i2c_line()
        bus_line_int = int(bus_line)
        bus = smbus.SMBus(bus_line_int)
        val = self.count_addr()

        if val == 2:
            bus_addr_int = 0x50
        if val == 1:
            bus_addr = self.find_address()
            bus_addr_int = int(bus_addr)

        H_Byte = 0x00
        L_Byte = 0x00
        bus.write_i2c_block_data(bus_addr_int, H_Byte, [L_Byte])
        binary_file = open("image.txt", "w")
        for i in range(0, res):
            read = bus.read_byte(bus_addr_int)
            print(read)
            read = str(read)
            binary_file.write(read)
            time.sleep(0.01)
        binary_file.close()
        print("end")
        self.pbar.setValue(100)


    #Verify chip
    def c5(self):
        val = self.line2.text()
        res = int(val)
        bus_line = self.find_i2c_line()
        bus_line_int = int(bus_line)
        bus = smbus.SMBus(bus_line_int)
        val = self.count_addr()

        if val == 2:
            bus_addr_int = 0x50
        if val == 1:
            bus_addr = self.find_address()
            bus_addr_int = int(bus_addr)

        H_Byte = 0x00
        L_Byte = 0x00
        bus.write_i2c_block_data(bus_addr_int, H_Byte, [L_Byte])
        binary_file = open("image.txt", "w")
        for i in range(0, res):
            read = bus.read_byte(bus_addr_int)
            print(read)
            read = str(read)
            binary_file.write(read)
            time.sleep(0.01)
        binary_file.close()
        print("end")
        self.pbar.setValue(100)
        print(file)
        with open('image.txt') as f1, open(file) as f2:
            for a, b in zip_longest(f1, f2):
                if a != b:
                    print('Файлы не равны')
                    break

# Auto chip
    def c6(self):
        print("!!!")


    def c7(self):
        print("!!!")
        global file
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './')
        if file:
            print(file)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
