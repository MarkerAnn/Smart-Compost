import sys
sys.path.append('/lib')  # Lägg till lib-mappen till sökvägarna

from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd

try:
    # Skapa en instans av I2C och LCD
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
    print("I2C initialized successfully")
    lcd = I2cLcd(i2c, 0x27, 2, 16)  # Använd I2C-adressen 0x27
    print("LCD initialized successfully")

    # Skriv en enkel text till LCD
    lcd.clear()
    lcd.putstr("Hello, World!")
    print("Text written to LCD")
except Exception as e:
    print("Failed to initialize I2C or LCD, or write text:", e)

# TODO: Delete this?