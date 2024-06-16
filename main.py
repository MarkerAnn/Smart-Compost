import sys
import time
import dht
from machine import Pin, I2C
from adafruit_scd4x import SCD4X
from sensors.lcd import LCD
from sensors.temperatureSensor import TemperatureSensor
from stemma_soil_sensor import StemmaSoilSensor  # Ändrad import

# Lägg till lib-mappen till sökvägarna
sys.path.append('/lib')

# Skriv ut sys.path för felsökning
print("sys.path i main.py:", sys.path)

# Skapa en instans av DHT11-sensorn
dht_sensor = dht.DHT11(Pin(16))

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

# Skapa en instans av SCD40-sensorn
scd40_sensor = SCD4X(i2c0)

# Starta periodisk mätning för SCD40
scd40_sensor.start_periodic_measurement()

# Vänta 30 sekunder för att säkerställa att SCD40-sensorn är redo
print("Waiting 30 seconds for the SCD40 sensor to stabilize...")
time.sleep(30)

# Felsökningsutskrifter för StemmaSoilSensor-initialisering
try:
    # Skapa en instans av StemmaSoilSensor för jordfuktighetssensorn
    print("Trying to initialize StemmaSoilSensor on address 0x36")
    soil_moisture_sensor = StemmaSoilSensor(i2c0, addr=0x36)
    print("StemmaSoilSensor initialized successfully")
except RuntimeError as e:
    print("Failed to initialize StemmaSoilSensor:", e)
    lcd.display_message("Soil sensor init error")
    soil_moisture_sensor = None
except Exception as e:
    print("An unexpected error occurred during StemmaSoilSensor initialization:", e)

# Funktion för att läsa sensordata och uppdatera LCD
def update_lcd_with_sensor_data():
    try:
        # Läs DHT11-data
        dht_sensor.measure()
        temperature_dht = dht_sensor.temperature()
        humidity_dht = dht_sensor.humidity()

        # Läs DS18B20-data
        soil_temperatures = soil_sensor.read_temperature()
        soil_temperature = soil_temperatures[0] if soil_temperatures else None

        # Läs SCD40-data
        if scd40_sensor.data_ready:
            co2 = scd40_sensor.co2
            temperature_scd = scd40_sensor.temperature
            humidity_scd = scd40_sensor.relative_humidity
        else:
            co2, temperature_scd, humidity_scd = None, None, None

        if soil_moisture_sensor:
            # Läs fuktighet från jordfuktighetssensorn
            soil_moisture = soil_moisture_sensor.get_moisture()
            print("Soil Moisture: {}".format(soil_moisture))  # Felsökningsutskrift
        else:
            soil_moisture = None

        # Skriv ut DHT11-data
        print("DHT11: Temp: {}C, Hum: {}%".format(temperature_dht, humidity_dht))
        if soil_temperature is not None:
            soil_temperature_formatted = "{:.1f}".format(soil_temperature)
            print("Soil: Temp: {}C".format(soil_temperature_formatted))
        if co2 is not None:
            print("CO2: {}ppm, Temp: {}C, Hum: {}%".format(co2, temperature_scd, humidity_scd))
            return temperature_dht, humidity_dht, soil_temperature_formatted, co2, temperature_scd, humidity_scd, soil_moisture
    except Exception as error:
        print("Exception occurred", error)
        lcd.display_message("Error reading sensors")
        return None

# Variabel för att hålla reda på vilken sida som visas
current_page = 0

# Funktion för att uppdatera LCD-sidor
def update_lcd_page(sensor_data):
    global current_page
    if sensor_data:
        temperature_dht, humidity_dht, soil_temperature, co2, temperature_scd, humidity_scd, soil_moisture = sensor_data
        lcd.lcd.clear()
        if current_page == 0:
            lcd.lcd.move_to(0, 0)
            lcd.lcd.putstr("CO2: {}ppm".format(co2))
            lcd.lcd.move_to(0, 1)
            lcd.lcd.putstr("Soil: {}C".format(soil_temperature))
        elif current_page == 1:
            lcd.lcd.move_to(6, 0)
            lcd.lcd.putstr("Air:")
            lcd.lcd.move_to(0, 1)
            lcd.lcd.putstr("{:.1f}C {:.1f}%".format(temperature_scd, humidity_scd))
        elif current_page == 2:
            lcd.lcd.move_to(6, 0)
            lcd.lcd.putstr("DHT:")
            lcd.lcd.move_to(0, 1)
            lcd.lcd.putstr("{}% {}C".format(humidity_dht, temperature_dht))
        elif current_page == 3 and soil_moisture is not None:
            lcd.lcd.move_to(0, 0)
            lcd.lcd.putstr("Soil Moisture:")
            lcd.lcd.move_to(0, 1)
            lcd.lcd.putstr(str(soil_moisture))
        current_page = (current_page + 1) % 4  # Växla till nästa sida

# Huvudloop
while True:
    sensor_data = update_lcd_with_sensor_data()
    update_lcd_page(sensor_data)
    time.sleep(5)
