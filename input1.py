import pygame
import sys
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
pygame.init()

pygame.display.set_mode((100, 100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                bytevals=[0XFF,127,0,0]
                checksum=(byteVals[1]+byteVals[2]+byteVals[3]) & 0X7F
                ser.write(bytearray([byteVals[0],byteVals[1],byteVals[2], byteVals[3],checksum]))
                print('Forward')
            elif event.key == pygame.K_s:
                bytevals=[0XFF,250,0,0]
                checksum=(byteVals[1]+byteVals[2]+byteVals[3]) & 0X7F
                ser.write(bytearray([byteVals[0],byteVals[1],byteVals[2], byteVals[3],checksum]))
                print('Backward')
