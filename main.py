from pathlib import Path

import smbus
import os
import subprocess
import sys
import time
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QProgressBar, QFileDialog)
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit

command_lsusb = "lsusb | grep 'Silicon Labs CP2112 HID I2C Bridge'"
command_find_i2c_line  = "i2cdetect -l | grep 'CP2112 SMBus Bridge'"
command_find_addr = "i2cdetect -y "
command_find_addr_50 = " | grep '50 -- '"
command_cat = "cat "
command_cat_verify = "cat image_verify.txt"



class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.col = QColor(50, 150, 255)

        discover_button = QPushButton('Discover chip', self)
        prog_button = QPushButton('Prog chip', self)
        erase_button = QPushButton('Erase chip', self)
        read_button = QPushButton('Read chip', self)
        verify_button = QPushButton('Verify chip', self)
        auto_button = QPushButton('Auto chip', self)

        discover_button.move(50, 90)
        prog_button.move(50, 130)
        erase_button.move(50, 170)
        read_button.move(50, 210)
        verify_button.move(50, 250)
        auto_button.move(50, 290)

        discover_button.clicked.connect(self.discover_action)
        prog_button.clicked.connect(self.prog_action)
        erase_button.clicked.connect(self.erase_action)
        read_button.clicked.connect(self.read_action)
        verify_button.clicked.connect(self.verify_action)
        auto_button.clicked.connect(self.auto_action)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Size bytes chip:')
        self.line = QLineEdit(self)

        self.line.move(120, 30)
        self.line.resize(200, 32)
        self.nameLabel.move(10, 35)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(50, 340, 200, 32)
        self.pbar.setValue(0)

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Eeprom prog 0.2 beta')
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
            #value = subprocess.check_output(command_find_50_addr, shell=True)
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
    def discover_action(self):
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
    def prog_action(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './')
        if file:
            print(file)
        val = self.line.text()
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
        address = 0x00

        min = 0
        max = 1

        file_prog = open(file, "rb")
        number = list(file_prog.read(1000))
        str(number)
        val = len(number)
        print(val)

        file_prog.close()
        for y in range(0, val):
            file_prog = open(file, "rb")
            number = list(file_prog.read(val))
            str(number)
            number = (number[min:max])
            print(number)
            list(map(int, number))
            s = [str(integer) for integer in number]
            a_string = "".join(s)
            res = int(a_string)
            print(res)
            print(type(res))
            min = min + 1
            max = max + 1
            file_prog.close()

            L_Byte_Data = [address, res]
            print(type(res), type(address))
            bus.write_i2c_block_data(bus_addr_int, H_Byte, L_Byte_Data)
            print(address)
            address = address + 1
            time.sleep(0.01)
        print("end")
        self.pbar.setValue(100)


#Erase chip
    def erase_action(self):
        val = self.line.text()
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
    def read_action(self):
        val = self.line.text()
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
        file = open("image_read.txt", "w")
        for i in range(0, res):
            read = bus.read_byte(bus_addr_int)
            read = chr(read)
            file.write(read)
            time.sleep(0.01)
        file.close()
        print("end")
        self.pbar.setValue(100)


    #Verify chip
    def verify_action(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './')
        if file:
            print(file)
        val = self.line.text()
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
        file_ver = open("image_verify.txt", "w")
        for i in range(0, res):
            read = bus.read_byte(bus_addr_int)
            #print(read)
            read = chr(read)
            file_ver.write(read)
            time.sleep(0.01)
        file_ver.close()
        print("end")

        cat_bin = Path(file).read_bytes()
        cat_verify = Path('image_verify.txt').read_bytes()
        cat_verify = cat_verify[:len(cat_bin)]
        print(cat_bin, cat_verify)
        if cat_bin == cat_verify:
            self.pbar.setValue(100)
        else:
            self.pbar.setValue(20)

# Auto chip
    def auto_action(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './')
        if file:
            print(file)

        # Erase chip
        val = self.line.text()
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
        data_00 = 0x00
        address = 0x00
        min = 0
        max = 1

        for y in range(0, res):
            L_Byte_Data = [address, data_00]
            bus.write_i2c_block_data(bus_addr_int, H_Byte, L_Byte_Data)
            print(address)
            address = address + 1
            time.sleep(0.01)
        print("Erase Chip")

        # Prog chip
        val = self.line.text()
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

        file_prog = open(file, "rb")
        number = list(file_prog.read(1000))
        str(number)
        val = len(number)
        print(val)

        file_prog.close()
        for y in range(0, val):
            file_prog = open(file, "rb")
            number = list(file_prog.read(val))
            str(number)
            number = (number[min:max])
            print(number)
            list(map(int, number))
            s = [str(integer) for integer in number]
            a_string = "".join(s)
            res = int(a_string)
            print(res)
            print(type(res))
            min = min + 1
            max = max + 1
            file_prog.close()

            L_Byte_Data = [address, res]
            print(type(res), type(address))
            bus.write_i2c_block_data(bus_addr_int, H_Byte, L_Byte_Data)
            print(address)
            address = address + 1
            time.sleep(0.01)
        print("Prog Chip")

        # Verify chip
        val = self.line.text()
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
        file_ver = open("image_verify.txt", "w")
        for i in range(0, res):
            read = bus.read_byte(bus_addr_int)
            #print(read)
            read = chr(read)
            file_ver.write(read)
            time.sleep(0.01)
        file_ver.close()
        print("end")

        cat_bin = Path(file).read_bytes()
        cat_verify = Path('image_verify.txt').read_bytes()
        cat_verify = cat_verify[:len(cat_bin)]
        print(cat_bin, cat_verify)
        if cat_bin == cat_verify:
            self.pbar.setValue(100)
            print("Verify Chip")
            print("Done !!!!!!!!!!!!")
        else:
            self.pbar.setValue(20)
            print("Verify Chip ERROR!!!")


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
