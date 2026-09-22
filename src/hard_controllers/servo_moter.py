import time
import RPi.GPIO as GPIO

class ServoMotor:
    def __init__(self, pin=18):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz
        self.pwm.start(0)
        self.current_angle = 90

    def set_angle(self, angle):
        """角度を 0〜180度 で設定 (SG90の制限)"""
        # 限界を超えないようにクリッピング
        angle = max(0.0, min(180.0, angle))
        self.current_angle = angle

        # SG90: 0度: 2.5%, 180度: 12.5% のデューティ比
        duty = 2.5 + (angle / 180.0) * 10.0
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.05)  # 追従時はスリープを短く設定 (0.15s -> 0.05s)
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)

    def track_target_with_imu(self, yaw_angle, base_angle=90.0):
        """
        IMUのYaw角(車体の傾き)に応じて、障害物の方向(正面90度基準)へ首を振り続ける
        yaw_angle > 0 (右旋回) ➔ サーボは左 (90 - yaw) へ向く
        yaw_angle < 0 (左旋回) ➔ サーボは右 (90 - yaw) へ向く
        """
        target_servo_angle = base_angle - yaw_angle
        # ±90度の旋回限界（0度〜180度）を超えないようガード
        target_servo_angle = max(0.0, min(180.0, target_servo_angle))
        
        self.set_angle(target_servo_angle)

    def cleanup(self):
        self.pwm.stop()