from fake_rpi.RPi import GPIO
import time

# ピン番号の設定
led_pin = 18

# GPIOの初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Lチカの実行
try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
