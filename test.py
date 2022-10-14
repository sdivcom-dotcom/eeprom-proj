import smbus
import time

bus = smbus.SMBus(16)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
Dev_Addr = 0x50  # 7 bit address (will be left shifted to add the read write bit)

data = 0xA0
address = 0x00

H_Byte = 0x00
L_Byte = 0x00

num = 5
min = 0
max = 1
def len_size():
    file = open("image.bin", "rb")
    number = list(file.read(200))
    str(number)
    val = len(number)
    #print(val)
    file.close()
    return val

val = len_size()

for y in range(0, val):
    file = open("image.bin", "rb")
    number = list(file.read(val))
    #str(number)
    number = (number[min:max])
    print(number)
    #list(map(int, number))
    s = [str(integer) for integer in number]
    a_string = "".join(s)
    res = int(a_string)
    print(res)
    print(type(res))
    min = min + 1
    max = max + 1
    file.close()
    L_Byte_Data = [address, res]
    print(type(res), type(address))
    bus.write_i2c_block_data(Dev_Addr, H_Byte, L_Byte_Data)
    print(address)
    address = address + 1
    time.sleep(0.01)

# Read Operation
bus.write_i2c_block_data(Dev_Addr, H_Byte, [L_Byte])
for i in range(0, 6):
    value = bus.read_byte(Dev_Addr)
    print(value)
    time.sleep(0.01)


print("end")
