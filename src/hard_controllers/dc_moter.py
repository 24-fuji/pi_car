from gpiozero import PWMOutputDevice
from time import sleep

# ピンの設定 (GPIO 12 と 13 を使用)
# PWMOutputDeviceを使うことで、0.0 〜 1.0 の値で速度（デューティ比）を指定できます
motor_in1 = PWMOutputDevice(12)
motor_in2 = PWMOutputDevice(13)

def motor_forward(speed):
    """正転: speedは 0.0 から 1.0"""
    motor_in1.value = speed
    motor_in2.value = 0

def motor_backward(speed):
    """逆転: speedは 0.0 から 1.0"""
    motor_in1.value = 0
    motor_in2.value = speed

def motor_stop():
    """停止"""
    motor_in1.value = 0
    motor_in2.value = 0

try:
    print("モーター制御開始: 速度を徐々に上げます")
    
    # 1. 徐々に加速 (正転)
    for s in [0.3, 0.5, 0.8, 1.0]:
        print(f"正転 速度: {s*100}%")
        motor_forward(s)
        sleep(2)

    # 2. 停止
    print("停止")
    motor_stop()
    sleep(1)

    # 3. 逆転
    print("逆転 速度: 50%")
    motor_backward(0.5)
    sleep(2)

except KeyboardInterrupt:
    # Ctrl+Cで安全に停止
    print("\n中断されました")

finally:
    motor_stop()
    print("終了")
