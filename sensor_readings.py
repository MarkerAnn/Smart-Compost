
def update_lcd_with_sensor_data(sensors):
    soil_sensor = sensors['soil_sensor']
    scd40_sensor = sensors['scd40_sensor']
    soil_moisture_sensor = sensors['soil_moisture_sensor']
    distance_sensor = sensors['distance_sensor']

    try:
        # Read DS18B20-data
        soil_temperatures = soil_sensor.read_temperature()
        soil_temperature = soil_temperatures[0] if soil_temperatures else None

        # Read SCD40-data
        if scd40_sensor.data_ready:
            co2 = scd40_sensor.co2
            temperature_scd = scd40_sensor.temperature
            humidity_scd = scd40_sensor.relative_humidity
        else:
            co2, temperature_scd, humidity_scd = None, None, None

        if soil_moisture_sensor:
            # Read mosture data
            try:
                soil_moisture = soil_moisture_sensor.get_moisture()
                print("Soil Moisture: {}".format(soil_moisture))  # Felsökningsutskrift
            except Exception as e:
                print("Failed to read soil moisture: ", e)
                soil_moisture = None
        else:
            soil_moisture = None

        # Read the distance from HC-SR04
        try:
            distance = distance_sensor.distance_cm()
            print("Distance: {} cm".format(distance)) 
        except Exception as e:
            print("Failed to read distance: ", e)
            distance = None

        if soil_temperature is not None:
            soil_temperature_formatted = "{:.1f}".format(soil_temperature)
            print("Soil: Temp: {}C".format(soil_temperature_formatted))
        if co2 is not None:
            print("CO2: {}ppm, Temp: {}C, Hum: {}%".format(co2, temperature_scd, humidity_scd))

        return {
            'soil_temperature': soil_temperature_formatted,
            'co2': co2,
            'temperature_scd': temperature_scd,
            'humidity_scd': humidity_scd,
            'soil_moisture': soil_moisture,
            'distance': distance
        }
    except Exception as error:
        print("Exception occurred", error)
        sensors['lcd'].display_message("Error reading sensors")
        return None