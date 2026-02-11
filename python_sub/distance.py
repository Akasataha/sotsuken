# python_sub/distance.py
import asyncio
import pigpio
import time


class DistanceSensor:
    def __init__(self, pi: pigpio.pi, trig: int, echo: int):
        self.pi = pi
        self.trig = trig
        self.echo = echo

        self.pi.set_mode(trig, pigpio.OUTPUT)
        self.pi.set_mode(echo, pigpio.INPUT)
        self.pi.write(trig, 0)

        self.speed_of_sound = 34370  # cm/s

    async def measure(self) -> float | None:
        # TRIG パルス
        self.pi.gpio_trigger(self.trig, 10, 1)

        start = None
        timeout = time.time() + 0.05

        # echo HIGH 待ち
        while time.time() < timeout:
            if self.pi.read(self.echo):
                start = self.pi.get_current_tick()
                break
            await asyncio.sleep(0)

        if start is None:
            return None

        # echo LOW 待ち
        while time.time() < timeout:
            if not self.pi.read(self.echo):
                end = self.pi.get_current_tick()
                dt = pigpio.tickDiff(start, end)
                return (dt / 1_000_000) * self.speed_of_sound / 2
            await asyncio.sleep(0)

        return None

    async def loop(self, queue: asyncio.Queue):
        try:
            while True:
                dist = await self.measure()
                if dist is not None:
                    await queue.put(dist)
                await asyncio.sleep(0.1)  # 10Hz
        except asyncio.CancelledError:
            raise
