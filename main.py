import smbus
import time
import os
import subprocess
import sys
import time
from datetime import datetime
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QFrame, QApplication, QProgressBar, QMessageBox, QTextBrowser, QFileDialog)
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit

command_find_i2c_line  = ""


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
        b5 = QPushButton('Auto chip', self)
        b6 = QPushButton('Add file', self)

        b1.move(50, 130)
        b2.move(50, 170)
        b3.move(50, 210)
        b4.move(50, 250)
        b5.move(50, 290)
        b6.move(50, 330)

        b1.clicked.connect(self.c1)
        b2.clicked.connect(self.c2)
        b3.clicked.connect(self.c3)
        b4.clicked.connect(self.c4)
        b5.clicked.connect(self.c5)
        b6.clicked.connect(self.c6)

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
        self.pbar.setGeometry(50, 360, 200, 100)
        self.pbar.setValue(0)

        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('CP2112 Eeprom prog')
        self.show()
#Find i2c line cp2112
    def find_i2c_line(self):
        os.system(command_find_i2c_line)
        val = subprocess.check_output(command_find_i2c_line, shell=True)
        print(val)
        return val.decode().strip()

#Find address chip
    def find_address(self):
        bus_find = self.find_i2c_line
        bus = smbus.SMBus(bus_find)
        val = bus.write_quick(0x50)
        if val == 0:
            addr = 0x50
            print(addr)
        else:
            addr = 0x00
        val = bus.write_quick(0x51)
        if val == 0:
            addr = 0x51
            print(addr)
        else:
            addr = 0x00
        val = bus.write_quick(0x52)
        if val == 0:
            addr = 0x52
            print(addr)
        else:
            addr = 0x00
        val = bus.write_quick(0x53)
        if val == 0:
            addr = 0x53
            print(addr)
        else:
            addr = 0x00
        return addr

    def c1(self):
        print("!!!")

    def c2(self):
        print("!!!")

    def c3(self):
        print("!!!")

    def c4(self):
        print("!!!")

    def c5(self):
        print("!!!")

    def c6(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './')

        if file:
            print(file)

def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

#bus = smbus.SMBus(16)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
#Dev_Addr = 0x50  # 7 bit address (will be left shifted to add the read write bit)

#data = 0xA1
#address = 0x00

#H_Byte = 0x00
#L_Byte = 0x00

#min_range = 0
#max_range = 128

# Write Operation

#for x in range(min_range, max_range):
 #   L_Byte_Data = [address, data]
    #bus.write_i2c_block_data(Dev_Addr, H_Byte, L_Byte_Data)
    #print(address)
    #address = address + 1
    #time.sleep(0.01)

# Read Operation
#bus.write_i2c_block_data(Dev_Addr, H_Byte, [L_Byte])
#for i in range(min_range, max_range):
    #value = bus.read_byte(Dev_Addr)
    #print(value)
    #time.sleep(0.01)

#print("end")

# Открываем на чтение бинарный файл
file = open("HMB-GD1-COEP540.fru.bin", "rb")
# Считываем в список первые 5 элементов
number = list(file.read(32768))
# Выводим список
print(number)
# Закрываем файл
file.close()