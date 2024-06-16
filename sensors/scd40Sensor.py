from machine import I2C
from scd40 import SCD40

class SCD40Sensor:
    def __init__(self, i2c):
        self.scd = SCD40(i2c)

    def read_measurements(self):
        if self.scd.data_ready():
            co2, temperature, humidity = self.scd.read_measurement()
            return co2, temperature, humidity
        else:
            return None, None, None
