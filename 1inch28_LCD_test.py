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

device_lcd1 = 1

device_lcd2 = 0



logging.basicConfig(level=logging.DEBUG)

def load_images(folder_path):

        images = []

        for filename in sorted(os.listdir(folder_path)):

            if filename.endswith(('.png', '.jpg', '.jpeg')):

                image_path = os.path.join(folder_path, filename)

                image = Image.open(image_path)

                image = image.resize((240, 240))

                images.append(image)

        return images



def draw_count_text(draw, font, count):

    draw.rectangle((0, 0, 240, 240), fill="BLACK")

    draw.text((90, 100), f"Count: {count}", fill="WHITE", font=font)



def count_to_100_lcd1():

    disp_lcd1 = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(0, 0), rst=27, dc=25, bl=18)

    disp_lcd1.Init()

    disp_lcd1.clear()

    images = []

    folder_path ='/home/a/bcm2835-1.71/WiringPi/LCD_Module_RPI_code/RaspberryPi/python/frames'

    for filename in sorted(os.listdir(folder_path)):

            if filename.endswith(('.png', '.jpg', '.jpeg')):

                image_path = os.path.join(folder_path, filename)

                image = Image.open(image_path)

                image = image.resize((240, 240))

                images.append(image)

                #images = sorted(images)

    for image in images:

        disp_lcd1.ShowImage(image.rotate(180))

        time.sleep(0.1)



    disp_lcd1.module_exit()



def count_to_minus_100_lcd2():

    disp_lcd2 = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(0, 1), rst=27, dc=25, bl=18)

    disp_lcd2.Init()

    disp_lcd2.clear()

    images = []

    folder_path ='/home/a/bcm2835-1.71/WiringPi/LCD_Module_RPI_code/RaspberryPi/python/frames'

    for filename in sorted(os.listdir(folder_path)):

            if filename.endswith(('.png', '.jpg', '.jpeg')):

                image_path = os.path.join(folder_path, filename)

                image = Image.open(image_path)

                image = image.resize((240, 240))

                images.append(image)

                #images = sorted(images)

    for image in images:

        disp_lcd2.ShowImage(image.rotate(180))

        time.sleep(0.1) 

    disp_lcd2.module_exit()



try: 



    # Create and start threads for counting on each LCD

    thread_lcd1 = threading.Thread(target=count_to_100_lcd1)



    thread_lcd2 = threading.Thread(target=count_to_minus_100_lcd2)



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

