import asyncio
import pigpio
from python_sub.sound import SoundPlayer

MOTOR_PIN = 21
STEER_PIN = 13

WIDTH_MAX = 2000
WIDTH_MIN = 1000
WIDTH_MID = 1500

SPEED_SUB = WIDTH_MAX - WIDTH_MID  # 500

STEER_MAX = 1700
STEER_MIN = 1300

STEER_SUB = STEER_MAX - WIDTH_MID  # 200


def search_command(sentence: str, commands: list):
    for command in commands:
        if command in sentence:
            return True
    else:
        return False


class Motors:
    def __init__(self, pi: pigpio.pi):
        self.pi = pi
        self.num_sp_m = {
            "1": 0.05,
            "2": 0.075,
            "3": 0.1,
            "4": 0.2,
            "5": 0.5,
        }
        self.num_sp_s = {
            "1": 0.2,
            "2": 0.4,
            "3": 0.6,
            "4": 0.8,
            "5": 1,
        }
        self.speed = 0.05  # 0~1
        self.direction = 0  # 1 or -1
        self.angle_power = 0.5  # 0~1
        self.angle = 0  # 1,0,-1
        self.set_width()
        self.set_motor(WIDTH_MID)
        self.set_steer(WIDTH_MID)

    def set_width(self):
        self.speed = max(min(self.speed, 1), 0)
        self.angle_power = max(min(self.angle_power, 1), 0)
        self.width_m = WIDTH_MID - (SPEED_SUB * self.direction * self.speed)
        self.width_s = WIDTH_MID + (STEER_SUB * self.angle * self.angle_power)

    def set_motor(self, width: int | float):
        width = max(min(width, WIDTH_MAX), 0)
        self.pi.set_servo_pulsewidth(MOTOR_PIN, width)

    def set_steer(self, width: int | float):
        width = max(min(width, STEER_MAX), STEER_MIN)
        self.pi.set_servo_pulsewidth(STEER_PIN, width)

    async def loop_task(self):
        try:
            while True:
                self.set_width()
                self.set_motor(self.width_m)
                self.set_steer(self.width_s)
                await asyncio.sleep(0.02)
        except asyncio.CancelledError:
            raise
        finally:
            self.set_motor(0)
            self.set_steer(WIDTH_MID)

    async def back(self):
        self.direction = -2.5
        await asyncio.sleep(0.2)
        self.direction = 0
        await asyncio.sleep(0.2)
        self.direction = -2.5

    async def breaking(self):
        if self.width_m < WIDTH_MID:
            self.direction = -100
            await asyncio.sleep(0.5)
        self.direction = 0

    async def debug(self):
        try:
            while True:
                print(
                    f"""
speed:{self.speed},widthm:{self.width_m}
anglep:{self.angle_power},widths:{self.width_s}
                      """
                )
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            raise

    async def distance_watcher(self, queue: asyncio.Queue):
        try:
            while True:
                dist = await queue.get()
                if (dist < 30) and (self.width_m < WIDTH_MID):
                    await self.breaking()
                    print(f"障害物発見:{dist:.1f}cm->ブレーキ")

        except asyncio.CancelledError:
            raise

    async def command_loop(self, queue: asyncio.Queue):
        try:
            while True:
                data = await queue.get()
                self.command(data)
        except asyncio.CancelledError:
            raise

    def command(self, data: dict):
        if float(data.get("cmscore1", 0)) > 0.1:
            print("認識結果:", data.get("sentence1", "データなんかねぇよ"))
            sentence = data.get("sentence1")
            if search_command(sentence, ["終了"]):
                pass  # self.mode=1
            elif search_command(sentence, ["開始"]):
                pass  # SoundPlayer.play("niture")
            elif search_command(sentence, ["前進", "進め", "進んで", "進行"]):
                if self.direction == 0:
                    self.direction = 1
                else:
                    self.direction = 0
            elif search_command(sentence, ["後退"]):
                asyncio.create_task(self.back())
            elif search_command(sentence, ["停止", "停車", "止まって"]):
                # SoundPlayer.play("theme")
                self.direction = 0
            elif search_command(sentence, ["ブレーキ", "ストップ", "止まれ"]):
                asyncio.create_task(self.breaking())
            elif search_command(sentence, ["前", "正面"]):
                self.angle = 0
            elif search_command(sentence, ["右", "右折"]):
                if self.angle > 0:
                    self.angle_power += 0.25
                else:
                    self.angle = 1
            elif search_command(sentence, ["左", "左折"]):
                if self.angle < 0:
                    self.angle_power += 0.25
                else:
                    self.angle = -1
            elif search_command(sentence, ["角度"]):
                if search_command(sentence, ["アップ", "上げて", "上がれ"]):
                    self.angle_power += 0.25
                elif search_command(sentence, ["ダウン", "下げて", "下がれ"]):
                    self.angle_power -= 0.25
                else:
                    for num in self.num_sp_s.keys():
                        if search_command(sentence, [num]):
                            self.angle_power = self.num_sp_s[num]
                            break
            elif search_command(sentence, ["スピード", "速度"]):
                if search_command(sentence, ["アップ", "上げて", "上がれ"]):
                    self.speed += 0.25
                elif search_command(sentence, ["ダウン", "下げて", "下がれ"]):
                    self.speed -= 0.25
                else:
                    for num in self.num_sp_m.keys():
                        if search_command(sentence, [num]):
                            self.speed = self.num_sp_m[num]
                            break
            elif search_command(sentence, ["加速", "早く"]):
                self.speed += 0.05
            elif search_command(sentence, ["減速", "ゆっくり"]):
                self.speed -= 0.05
            else:
                self.direction = 0

        else:
            print("認識失敗")
