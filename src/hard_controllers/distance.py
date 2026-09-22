import time
import RPi.GPIO as GPIO

class DistanceSensor:
    def __init__(self, trig_pin=23, echo_pin=24):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.last_time = 0
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, False)
        time.sleep(0.5)

    def get_distance(self):
        """距離[cm]を取得 (測定間隔200msを考慮)"""
        now = time.time()
        if now - self.last_time < 0.2:
            time.sleep(0.2 - (now - self.last_time))
        self.last_time = time.time()

        # パルス送信
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        pulse_start = time.time()
        pulse_end = time.time()

        timeout = time.time() + 0.04  # タイムアウト設定
        while GPIO.input(self.echo_pin) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return 999.0  # 測定不能時

        while GPIO.input(self.echo_pin) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return 999.0

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # 音速 343m/s ÷ 2
        return round(distance, 2)

    def cleanup(self):
        pass