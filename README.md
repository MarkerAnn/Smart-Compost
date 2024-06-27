# Compost Monitoring System

## Overview

This project is designed to monitor compost conditions using various sensors connected to a microcontroller unit. It utilizes the ESP32/ESP8266 chipset to read environmental data (e.g., temperature, humidity), display information on an LCD, and publish the data to an MQTT broker hosted on AWS IoT Core.

You can find more information [here](https://hackmd.io/@3KzL4qeKQkifnP_tzEbLJQ/SJv5nV9LC)

Frontend code can be find [here](https://github.com/MarkerAnn/smart_compost_frontend.git)

## Features

- Wi-Fi connectivity to transmit data securely.
- Real-time sensor data collection and display on an LCD.
- MQTT communication for data publishing.
- Automatic time synchronization with NTP servers.
- Error handling for connectivity and sensor failures.

## Prerequisites

- Python 3.x
- ESP32 or ESP8266 microcontroller
- MQTT broker credentials and setup (AWS IoT Core recommended)
- Necessary Python libraries installed in the microcontroller, including `umqtt.simple` and `machine`

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```
2. **Setup the MQTT broker:**

   - Obtain MQTT credentials from AWS IoT Core (Certificate, Private Key, and CA file).
   - Place these files in the `certs` directory.

3. **Configure the device:**

   - Rename `config_example.py` to `config.py`.
   - Update `config.py` with your Wi-Fi credentials and AWS IoT Core endpoint.

4. **Deploy the code:**
   - Upload all Python files to your microcontroller using a suitable uploader tool like Thonny or esptool.

## Configuration Files

- `config.py`: Contains configuration for Wi-Fi and AWS IoT Core settings.
- `certs/`: Directory to store SSL/TLS certificates.

## Usage

Execute the main script after configuration to start reading sensor data and transmitting it to the configured MQTT broker.

### Functions

- **`connect_internet()`**: Connects to the Internet via Wi-Fi.
- **`sync_time()`**: Synchronizes device time with NTP.
- **`initialize_mqtt_client()`**: Initializes and returns an MQTT client configured with SSL.
- **`publish_sensor_data()`**: Publishes sensor data to a specific MQTT topic.

## Sensors

This system is configured to work with generic temperature, humidity, and other environmental sensors. Modify the `sensor_setup.py` script according to your specific sensor setup.
