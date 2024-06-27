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

# Add 'lib' folder to the paths
sys.path.append('/lib')

# Print sys.path for debugging
print("sys.path in main.py:", sys.path)

# Wi-Fi and MQTT settings
SSID = config.SSID
WIFI_PASSWORD = config.WIFI_PASSWORD
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()
MQTT_CLIENT_KEY = 'certs/aws_private.der'
MQTT_CLIENT_CERT = 'certs/aws_cert.der'
MQTT_BROKER_CA = 'certs/aws_ca.der'
MQTT_BROKER = config.IOT_CORE_ENDPOINT

# Initialize sensors
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

if not key or not cert or not ca:
    print("Failed to read one or more DER files. Exiting.")
    sys.exit()

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        for attempt in range(10):
            if wlan.isconnected():
                print('Connected to WiFi. IP:', wlan.ifconfig()[0])
                return True
            time.sleep(1)
        print('Failed to connect to WiFi')
        return False
    else:
        print('Already connected to WiFi.')
        return True

def disconnect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        wlan.active(False)
        print('Disconnected from WiFi')

def sync_time(retries=5, delay=5):
    for attempt in range(retries):
        try:
            print("Synchronizing time with NTP server...")
            ntptime.settime()  # This will set the RTC with the NTP time
            print("Time synchronized")
            return True
        except Exception as e:
            print(f"Failed to synchronize time on attempt {attempt + 1}: {e}")
            time.sleep(delay)
    print("Failed to synchronize time after multiple attempts.")
    return False

def initialize_mqtt_client():
    client = MQTTClient(
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
        })
    return client

def publish_sensor_data(sensor_readings, mqtt_client):
    try:
        mqtt_message = json.dumps(sensor_readings)
        print(f"Attempting to publish data to topic 'pico_w/compost_data': {mqtt_message}")
        mqtt_client.publish("pico_w/compost_data", mqtt_message)
        print(f"Published data: {mqtt_message}")
    except Exception as e:
        print(f"Failed to publish data: {e}")
    finally:
        mqtt_client.disconnect()
        print("Disconnected from MQTT broker")

# Connect to Wi-Fi and Sync Time
if connect_wifi(SSID, WIFI_PASSWORD):
    time_synchronized = sync_time()

# Variable to keep track of which page is being displayed
current_page = 0

# Variable to store the latest sensor values
sensor_readings = {}

# Main loop
MEASUREMENT_INTERVAL = 21600  # Measure sensor data every 6 hours
last_page_update_time = time.time()
last_measurement_time = time.time() - MEASUREMENT_INTERVAL  # First measurement should happen immediately

while True:
    current_time = time.time()

    # Update the LCD display every 10 seconds
    if current_time - last_page_update_time >= 10:
        if sensor_readings:
            update_lcd_page(sensor_readings, sensors['lcd'], current_page)
            current_page = (current_page + 1) % 4  # Cycle through pages 0-3
            last_page_update_time = current_time

    # Collect and publish sensor data every MEASUREMENT_INTERVAL seconds
    if current_time - last_measurement_time >= MEASUREMENT_INTERVAL:
        if connect_wifi(SSID, WIFI_PASSWORD):
            mqtt_client = initialize_mqtt_client()
            print("Connecting to MQTT broker")
            try:
                mqtt_client.connect()
                print("Connected to MQTT broker")
                new_sensor_readings = update_lcd_with_sensor_data(sensors)
                if new_sensor_readings:
                    sensor_readings = new_sensor_readings
                    print(f"New sensor readings: {sensor_readings}")
                    publish_sensor_data(sensor_readings, mqtt_client)
            except Exception as e:
                print(f"Failed to connect to MQTT broker: {e}")
            disconnect_wifi()
        last_measurement_time = current_time

    time.sleep(1)  # Wait a second before next iteration
