import pigpio


class GpioManager:
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpiodデーモンが起動していません。")

    def close(self):
        self.pi.stop()
