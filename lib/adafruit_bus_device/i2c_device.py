class I2CDevice:
    def __init__(self, i2c, device_address):
        self.i2c = i2c
        self.device_address = device_address

        # Kontrollera att enheten är närvarande
        try:
            self.i2c.writeto(self.device_address, b'')
        except OSError:
            raise ValueError("No I2C device at address: 0x%x" % self.device_address)

    def readinto(self, buf, *, start=0, end=None):
        if end is None:
            end = len(buf)
        self.i2c.readfrom_into(self.device_address, buf[start:end])

    def write(self, buf, *, start=0, end=None):
        if end is None:
            end = len(buf)
        self.i2c.writeto(self.device_address, buf[start:end])

    def write_then_readinto(self, out_buffer, in_buffer, *, out_start=0, out_end=None, in_start=0, in_end=None):
        if out_end is None:
            out_end = len(out_buffer)
        if in_end is None:
            in_end = len(in_buffer)
        self.i2c.writeto_then_readfrom(self.device_address, out_buffer, in_buffer, out_start=out_start, out_end=out_end, in_start=in_start, in_end=in_end)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
