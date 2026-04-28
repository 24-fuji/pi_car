from gpiozero import LED
from time import sleep

# GPIO 17番ピンを指定
led = LED(17)

try:
    while True:
        led.on()       # 点灯
        print("LED ON")
        sleep(1)
        
        led.off()      # 消灯
        print("LED OFF")
        sleep(1)

except KeyboardInterrupt:
    led.off() # 終了時に消灯

# from gpiozero import PWMLED
# from time import sleep

# led = PWMLED(17)

# try:
#     while True:
#         # 徐々に明るく
#         for i in range(101):
#             led.value = i / 100
#             sleep(0.01)
#         # 徐々に暗く
#         for i in range(100, -1, -1):
#             led.value = i / 100
#             sleep(0.01)

# except KeyboardInterrupt:
#     led.off()