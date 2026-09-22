from gpiozero import Servo
from time import sleep

# GPIO 18番ピンを使用
# SG90のパルス幅に合わせて微調整（min=0.5ms, max=2.4ms程度）
servo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)

try:
    while True:
        print("Min")
        servo.min()  # 約 -90度
        sleep(1)
        
        print("Mid")
        servo.mid()  # 0度（中央）
        sleep(1)
        
        print("Max")
        servo.max()  # 約 +90度
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped")