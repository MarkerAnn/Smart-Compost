# boot.py -- run on boot-up
import network
import time
import config

# WiFi settings
SSID = config.SSID
WIFI_PASSWORD = config.WIFI_PASSWORD

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, WIFI_PASSWORD)

# Kontrollera anslutningen
max_attempts = 10
attempts = 0
while not wlan.isconnected() and attempts < max_attempts:
    attempts += 1
    print('Connecting to WiFi...')
    time.sleep(1)

if wlan.isconnected():
    print('Connected to WiFi')
    print('IP Address:', wlan.ifconfig()[0])
else:
    print('Failed to connect to WiFi')
