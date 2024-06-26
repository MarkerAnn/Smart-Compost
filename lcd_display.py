def update_lcd_page(sensor_data, lcd, current_page):
    soil_temperature = sensor_data.get('soil_temperature')
    co2 = sensor_data.get('co2')
    temperature_scd = sensor_data.get('temperature_scd')
    humidity_scd = sensor_data.get('humidity_scd')
    soil_moisture = sensor_data.get('soil_moisture')
    distance = sensor_data.get('distance')

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
    elif current_page == 2 and soil_moisture is not None:
        lcd.lcd.move_to(0, 0)
        lcd.lcd.putstr("Soil Moisture:")
        lcd.lcd.move_to(0, 1)
        lcd.lcd.putstr(str(soil_moisture))
    elif current_page == 3 and distance is not None:
        lcd.lcd.move_to(0, 0)
        lcd.lcd.putstr("Distance:")
        lcd.lcd.move_to(0, 1)
        lcd.lcd.putstr("{:.1f} cm".format(distance))

def lcd_clear(lcd):
    """
    Rensar LCD-skärmen.
    """
    lcd.lcd.clear()  # Anta att ditt LCD-objekt har en clear-metod

def lcd_message(lcd, message):
    """
    Visar ett meddelande på LCD-skärmen.
    """
    lcd.lcd.clear()  # Rensa skärmen innan du skriver nytt meddelande
    lcd.lcd.putstr(message)  # Anta att ditt LCD-objekt har en putstr-metod för att skriva text
