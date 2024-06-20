import sys
import time
import json
import machine
import network
import ssl
import ubinascii
import ntptime
from umqtt.simple import MQTTClient
import config
from sensor_setup import setup_sensors
from lcd_display import update_lcd_page
from sensor_readings import update_lcd_with_sensor_data

# Lägg till lib-mappen till sökvägarna
sys.path.append('/lib')

# Skriv ut sys.path för felsökning
print("sys.path i main.py:", sys.path)

# Wi-Fi och MQTT-inställningar
SSID = config.SSID
WIFI_PASSWORD = config.WIFI_PASSWORD
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()
MQTT_CLIENT_KEY = 'certs/aws_private.der'
MQTT_CLIENT_CERT = 'certs/aws_cert.der'
MQTT_BROKER_CA = 'certs/aws_ca.der'
MQTT_BROKER = config.IOT_CORE_ENDPOINT

# Initiera I2C och sensorer
sensors = setup_sensors()

def read_der(file):
    try:
        with open(file, "rb") as input:
            der_data = input.read()
        print(f"Successfully read {file}")
        return der_data
    except Exception as e:
        print(f"Error reading {file}: {e}")
        return None

key = read_der(MQTT_CLIENT_KEY)
cert = read_der(MQTT_CLIENT_CERT)
ca = read_der(MQTT_BROKER_CA)

print("Key content (DER):", key)
print("Cert content (DER):", cert)
print("CA content (DER):", ca)

def connect_internet():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, WIFI_PASSWORD)
    for _ in range(10):
        if sta_if.isconnected():
            print("Connected to Wi-Fi")
            return
        time.sleep(1)
    print("Could not connect to Wi-Fi")

def sync_time():
    try:
        print("Synchronizing time with NTP server...")
        ntptime.settime()  # This will set the RTC with the NTP time
        print("Time synchronized")
    except Exception as e:
        print("Failed to synchronize time:", e)

def publish_sensor_data(sensor_readings, mqtt_client):
    try:
        mqtt_message = json.dumps(sensor_readings)
        mqtt_client.publish("pico_w/compost_data", mqtt_message)  # Ändra detta till ditt ämne
        print(f"Published data: {mqtt_message}")
    except Exception as e:
        print(f"Failed to publish data: {e}")

# Anslut till Wi-Fi
connect_internet()

# Synkronisera tid
sync_time()

# Kontrollera att nyckel, certifikat och CA laddades korrekt
if not key or not cert or not ca:
    print("Failed to read one or more DER files. Exiting.")
    sys.exit()

# Initiera MQTT-klienten
mqtt_client = MQTTClient(
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    keepalive=60,
    ssl=True,
    ssl_params={
        "key": key,
        "cert": cert,
        "server_hostname": MQTT_BROKER,
        "cert_reqs": ssl.CERT_REQUIRED,
        "cadata": ca,
    },
)

# Anslut till MQTT
print("Connecting to MQTT broker")
try:
    mqtt_client.connect()
    print("Connected to MQTT broker")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    sys.exit()

# Variabel för att hålla reda på vilken sida som visas
current_page = 0

# Huvudloop
while True:
    sensor_readings = update_lcd_with_sensor_data(sensors)
    if sensor_readings:
        update_lcd_page(sensor_readings, sensors['lcd'], current_page)
        current_page = (current_page + 1) % 4  # Växla till nästa sida
        publish_sensor_data(sensor_readings, mqtt_client)  # Publicera sensorvärden
    time.sleep(5)
