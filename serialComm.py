import time
import serial

#!/bin/bash

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

byteVals=bytearray(input('Enter string'))
#print byteVals[0]

for i in range(1,4):
    if byteVals[i]>255:
        byteVals[i]=255
   
checksum=(byteVals[1]+byteVals[2]+byteVals[3]) & 0X7F
print checksum

if ser.isOpen():
    print(ser.name+' is open')
print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1

# send the character to the device
# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
#print(input)
#print type(bytearray([0XFF, 0, 0,0,0]))
ser.write((bytearray([byteVals[0],byteVals[1],byteVals[2], byteVals[3],checksum])))
out = ''
# let's wait one second before reading output (let's give device time to answer)
time.sleep(1)
while ser.inWaiting() > 0:
    print 'i'
    out += ser.read(1)

if out != '':
    print ">>" +out
            
