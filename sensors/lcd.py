import sys
sys.path.append('/lib')  # Add the lib folder to the path

from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
import utime

# Class to handle the LCD
class LCD:
    def __init__(self, i2c, i2c_addr=0x27, rows=2, cols=16):
        try:
            self.i2c = i2c
            self.lcd = I2cLcd(self.i2c, i2c_addr, rows, cols)
            print("LCD init success")
        except Exception as e:
            print("Failed to initialize LCD:", e)

    # Function to display a message on the LCD
    def display_message(self, message):
        try:
            self.lcd.clear()
            self.lcd.putstr(message)
            print("Message displayed on LCD:", message)
        except Exception as e:
            print("Failed to display message on LCD:", e)
    
    # Function to move the cursor on the LCD
    def move_to(self, col, row):
        try:
            self.lcd.move_to(col, row)
        except Exception as e:
            print("Failed to move cursor on LCD:", e)
    
    # Function to write a string at the current cursor position
    def putstr(self, string):
        try:
            self.lcd.putstr(string)
        except Exception as e:
            print("Failed to write string to LCD:", e)
    
    # Function to turn off the LCD backlight
    def backlight_off(self):
        try:
            self.lcd.backlight_off()
        except Exception as e:
            print("Failed to turn off backlight:", e)
