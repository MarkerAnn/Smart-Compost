import time
from machine import Pin, I2C
from adafruit_scd4x import SCD4X
from sensors.lcd import LCD
from sensors.temperatureSensor import TemperatureSensor
from stemma_soil_sensor import StemmaSoilSensor
from hcsr04 import HCSR04

def setup_sensors():
    # Skapa en instans av TemperatureSensor för DS18B20-sensorn
    soil_sensor = TemperatureSensor(4)

    # Skapa en instans av I2C0 (använd samma I2C-buss för alla enheter)
    i2c0 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

    # Skanna I2C0-bussen och skriv ut adresser
    print("I2C0 scan result:", i2c0.scan())

    # Skapa en instans av LCD
    try:
        lcd = LCD(i2c0)  # Använd den gemensamma I2C-instansen
        print("LCD init success")
    except Exception as e:
        print("Failed to initialize LCD:", e)
        lcd = None

    # Skapa en instans av SCD40-sensorn
    scd40_sensor = SCD4X(i2c0)

    # Starta periodisk mätning för SCD40
    scd40_sensor.start_periodic_measurement()

    # Vänta 10 sekunder för att säkerställa att SCD40-sensorn är redo
    # print("Waiting 10 seconds for the SCD40 sensor to stabilize...")
    # time.sleep(10)

    # Skapa en instans av StemmaSoilSensor för jordfuktighetssensorn
    try:
        print("Trying to initialize StemmaSoilSensor on address 0x36")
        soil_moisture_sensor = StemmaSoilSensor(i2c0, addr=0x36)
        print("StemmaSoilSensor initialized successfully")
    except RuntimeError as e:
        print("Failed to initialize StemmaSoilSensor:", e)
        lcd.display_message("Soil sensor init error")
        soil_moisture_sensor = None
    except Exception as e:
        print("An unexpected error occurred during StemmaSoilSensor initialization:", e)
        soil_moisture_sensor = None

    # Skapa en instans av HCSR04 för HC-SR04
    distance_sensor = HCSR04(trigger_pin=22, echo_pin=21)  # Anpassa till rätt pinnar

    return {
        'soil_sensor': soil_sensor,
        'lcd': lcd,
        'scd40_sensor': scd40_sensor,
        'soil_moisture_sensor': soil_moisture_sensor,
        'distance_sensor': distance_sensor
    }
