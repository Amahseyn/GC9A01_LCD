import os
import sys
sys.path.append("..")
import time
import logging
import spidev as SPI
from lib import LCD_1inch28
from PIL import Image
import threading

# Raspberry Pi pin configuration:
RST = 27
DC = 24
BL = 18
bus = 0

logging.basicConfig(level=logging.DEBUG)

def draw_count_text(draw, font, count):
    draw.rectangle((0, 0, 240, 240), fill="BLACK")
    draw.text((90, 100), f"Count: {count}", fill="WHITE", font=font)

def count_to_100_lcd1(lock):
    disp_lcd1 = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(0, 0), rst=24, dc=25, bl=18)
    disp_lcd2 = LCD_1inch28.LCD_1inch28(spi=SPI.SpiDev(1, 2), rst=6, dc=26, bl=22)
    disp_lcd1.Init()
    disp_lcd2.Init()
    disp_lcd1.clear()
    disp_lcd2.clear()
    images = []
    folder_path = '/home/a/bcm2835-1.71/WiringPi/LCD_Module_RPI_code/RaspberryPi/python/frames'
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            image = Image.open(image_path)
            image = image.resize((240, 240))
            images.append(image)
    
    lock.acquire()
    try:
        for i in range(100):
            for image in images:
                disp_lcd1.ShowImage(image.rotate(180))
                disp_lcd2.ShowImage(image.rotate(180))
                time.sleep(.5)
    finally:
        lock.release()

    disp_lcd1.module_exit()
    disp_lcd2.module_exit()

if __name__ == "__main__":
    lock = threading.Lock()
    
    thread_lcd1 = threading.Thread(target=count_to_100_lcd1, args=(lock,))
    thread_lcd2 = threading.Thread(target=count_to_100_lcd1, args=(lock,))

    thread_lcd1.start()
    thread_lcd2.start()

    thread_lcd1.join()
    thread_lcd2.join()

    logging.info("quit:")
