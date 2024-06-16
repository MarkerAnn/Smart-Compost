import time
from machine import Pin
import onewire, ds18x20

class TemperatureSensor:
    def __init__(self, pin):
        self.ow = onewire.OneWire(Pin(pin))
        self.ds = ds18x20.DS18X20(self.ow)
        self.roms = self.ds.scan()
        print('Found DS devices: ', self.roms)

    def read_temperature(self):
        self.ds.convert_temp()
        time.sleep_ms(750)
        temperatures = []
        for rom in self.roms:
            temperatures.append(self.ds.read_temp(rom))
        return temperatures