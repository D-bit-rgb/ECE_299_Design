
from machine import Pin, I2C

class Radio:
    def __init__(self, freq, vol, mute):
        self.Volume = 2
        self.Frequency = 88
        self.Mute = False

        self.SetVolume(vol)
        self.SetFrequency(freq)
        self.SetMute(mute)

        self.i2c_sda = Pin(26)
        self.i2c_scl = Pin(27)
        self.i2c_device = 1
        self.i2c_device_address = 0x10
        self.Settings = bytearray(8)
        self.radio_i2c = I2C(self.i2c_device, scl=self.i2c_scl, sda=self.i2c_sda, freq=200000)
        self.ProgramRadio()

    def SetVolume(self, v):
        try:
            v = int(v)
            if 0 <= v < 16:
                self.Volume = v
                return True
        except:
            pass
        return False

    def SetFrequency(self, f):
        try:
            f = float(f)
            if 88.0 <= f <= 108.0:
                self.Frequency = f
                return True
        except:
            pass
        return False

    def SetMute(self, m):
        try:
            self.Mute = bool(int(m))
            return True
        except:
            return False

    def ComputeChannelSetting(self, f):
        f = int(f * 10) - 870
        return bytearray([(f >> 2) & 0xFF, ((f & 0x03) << 6) & 0xC0])

    def UpdateSettings(self):
        self.Settings[0] = 0x80 if self.Mute else 0xC0
        self.Settings[1] = 0x09 | 0x04
        self.Settings[2:4] = self.ComputeChannelSetting(self.Frequency)
        self.Settings[3] |= 0x10
        self.Settings[4] = 0x04
        self.Settings[5] = 0x00
        self.Settings[6] = 0x84
        self.Settings[7] = 0x80 + self.Volume

    def ProgramRadio(self):
        self.UpdateSettings()
        self.radio_i2c.writeto(self.i2c_device_address, self.Settings)
