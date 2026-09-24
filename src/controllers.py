import time
import RPi.GPIO as GPIO

from hard_controllers.distance import DistanceSensor
from hard_controllers.servo_moter import ServoMotor
from hard_controllers.dc_moter import DRV8835DualMotor
from hard_controllers.imu import MPU6050
from soft_controllers.path_planner import PathPlanner

class MainController:
    def __init__(self):
        self.sensor = DistanceSensor()
        self.servo = ServoMotor()
        self.motor = DRV8835DualMotor()  # 固定されたDRV8835クラスを使用
        self.imu = MPU6050()
        self.planner = PathPlanner(self.motor, self.imu)

        self.state = "SCAN_FRONT"
        self.servo.set_angle(90)  # 正面

    def analyze_scan_data(self, scan_data):
        distances = [d for a, d in scan_data if d > 0]
        close_count = sum(1 for d in distances if d < 30.0)

        if close_count >= 4:
            return "WALL"
        elif close_count in [1, 2]:
            return "POLE"
        else:
            return "OTHER"

    def run(self):
        try:
            current_dist = 0.0
            while True:
                # IMU角度更新（常時）
                current_yaw = self.imu.update()

                # --- State 1: 正面監視（通常前進） ---
                if self.state == "SCAN_FRONT":
                    self.servo.set_angle(90)
                    current_dist = self.sensor.get_distance()
                    
                    if current_dist < 25.0:
                        self.motor.stop()
                        self.state = "SWEEP_SCAN"
                    else:
                        # 通常前進 (40% PWM)
                        self.motor.set_motor_left(0.4)
                        self.motor.set_motor_right(0.4)

                # --- State 2: 首振りスキャン ➔ 判定 ---
                elif self.state == "SWEEP_SCAN":
                    # スキャン開始時に改行を入れて表示を分ける
                    print("\n[Sweep Scanning...]")
                    scan_data = []
                    for angle in [30, 60, 90, 120, 150]:
                        self.servo.set_angle(angle)
                        d = self.sensor.get_distance()
                        scan_data.append((angle, d))
                        # スキャン中の状態もリアルタイム表示
                        print(f"\r[SCAN] Servo: {angle:>3.0f}deg | Dist: {d:>5.1f}cm", end="", flush=True)
                    
                    self.servo.set_angle(90)
                    target_type = self.analyze_scan_data(scan_data)
                    print(f"\n[Scan Result] Detected: {target_type}")

                    self.planner.start_action()
                    if target_type == "WALL":
                        self.state = "ACTION_BACK"
                    elif target_type == "POLE":
                        self.state = "ACTION_AVOID_CIRCLE"
                    else:
                        self.state = "ACTION_TURN_180"

                # --- State 3: 壁 ➔ バック動作 ---
                elif self.state == "ACTION_BACK":
                    if self.planner.execute_back(duration=1.2):
                        self.state = "SCAN_FRONT"

                # --- State 4: 棒 ➔ 円軌道回避動作 ---
                elif self.state == "ACTION_AVOID_CIRCLE":
                    # 車体が傾いた分だけサーボを回し、常に棒を追従
                    self.servo.track_target_with_imu(current_yaw, base_angle=90.0)

                    if self.planner.execute_circle_avoidance():
                        self.servo.set_angle(90)
                        self.state = "SCAN_FRONT"

                # --- State 5: その他 ➔ 180度旋回 ---
                elif self.state == "ACTION_TURN_180":
                    if self.planner.execute_turn_180():
                        self.state = "SCAN_FRONT"

                # --- コマンドラインリアルタイム表示 (上書き更新) ---
                servo_deg = getattr(self.servo, "current_angle", 90.0)
                status_msg = (
                    f"\rState: {self.state:<19} | "
                    f"IMU Yaw: {current_yaw:>6.1f}deg | "
                    f"Dist: {current_dist:>5.1f}cm | "
                    f"Servo: {servo_deg:>5.1f}deg"
                )
                print(status_msg, end="", flush=True)

                time.sleep(0.02)  # 50Hz周期

        except KeyboardInterrupt:
            print("\nStopping robot...")
        finally:
            self.motor.close()  # DRV8835DualMotor の終了処理
            self.servo.cleanup()
            self.sensor.cleanup()
            GPIO.cleanup()

if __name__ == "__main__":
    controller = MainController()
    controller.run()
