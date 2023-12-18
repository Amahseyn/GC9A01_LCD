#!/usr/bin/python

# -*- coding: UTF-8 -*-

import os

import sys

sys.path.append("..")



import time

import logging

import spidev as SPI

from lib import LCD_1inch28

from PIL import Image, ImageDraw, ImageFont

import threading



# Raspberry Pi pin configuration:

RST = 27

DC = 25

BL = 18

bus = 0

device_lcd1 = 0

device_lcd2 = 1



logging.basicConfig(level=logging.DEBUG)



def draw_count_text(draw, font, count):

    draw.rectangle((0, 0, 240, 240), fill="BLACK")

    draw.text((90, 100), f"Count: {count}", fill="WHITE", font=font)



def count_to_10_lcd1(disp_lcd1):

    image1 = Image.new("RGB", (disp_lcd1.width, disp_lcd1.height), "BLACK")

    draw1 = ImageDraw.Draw(image1)

    font = ImageFont.load_default()



    for count1 in range(100,200):

        draw_count_text(draw1, font, count1)

        disp_lcd1.ShowImage(image1.rotate(180))

        time.sleep(.1)



    disp_lcd1.module_exit()



def count_to_minus_10_lcd2(disp_lcd2):

    image2 = Image.new("RGB", (disp_lcd2.width, disp_lcd2.height), "BLACK")

    draw2 = ImageDraw.Draw(image2)

    font = ImageFont.load_default()



    for count2 in range(0, -100, -1):

        draw_count_text(draw2, font, count2)

        disp_lcd2.ShowImage(image2.rotate(180))

        time.sleep(.1)



    disp_lcd2.module_exit()



try:

    # Display with hardware SPI:

    disp_lcd1 = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device_lcd1), rst=RST, dc=DC, bl=BL)

    disp_lcd2 = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(bus, device_lcd2), rst=RST, dc=DC, bl=BL)



    # Initialize libraries.

    disp_lcd1.Init()

    disp_lcd2.Init()



    # Clear displays.

    disp_lcd1.clear()

    disp_lcd2.clear()



    # Create and start threads for counting on each LCD

    thread_lcd1 = threading.Thread(target=count_to_10_lcd1, args=(disp_lcd1,))

    thread_lcd2 = threading.Thread(target=count_to_minus_10_lcd2, args=(disp_lcd2,))



    thread_lcd1.start()

    thread_lcd2.start()



    # Wait for both threads to finish

    thread_lcd1.join()

    thread_lcd2.join()



    logging.info("quit:")



except IOError as e:

    logging.info(e)

except KeyboardInterrupt:

    disp_lcd1.module_exit()

    disp_lcd2.module_exit()

    logging.info("quit:")

    sys.exit()

