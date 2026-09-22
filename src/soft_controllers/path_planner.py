import time

class PathPlanner:
    def __init__(self, motor, imu):
        self.motor = motor
        self.imu = imu
        self.step_state = 0
        self.start_time = 0

    def start_action(self):
        self.step_state = 0
        self.start_time = time.time()
        self.imu.reset_yaw()

    def execute_back(self, duration=1.2):
        """指定時間だけ直線バック (速度 -0.4)"""
        if time.time() - self.start_time < duration:
            self.motor.set_motor_left(-0.4)
            self.motor.set_motor_right(-0.4)
            return False
        else:
            self.motor.stop()
            return True

    def execute_turn_180(self):
        """IMUのYaw角を見ながら180度超信地旋回"""
        current_yaw = abs(self.imu.get_yaw())
        if current_yaw < 170.0:  # 170度目標
            self.motor.set_motor_left(-0.5)
            self.motor.set_motor_right(0.5)
            return False
        else:
            self.motor.stop()
            return True

    def execute_circle_avoidance(self):
        """円関数的S字軌道による回避動作 (IMU FB付き)"""
        current_yaw = self.imu.get_yaw()

        if self.step_state == 0:
            # 右旋回（左タイヤ強, 右タイヤ弱）
            if current_yaw > -35.0:
                self.motor.set_motor_left(0.6)
                self.motor.set_motor_right(0.2)
                return False
            else:
                self.step_state = 1

        elif self.step_state == 1:
            # 逆向きに左旋回
            if current_yaw < 35.0:
                self.motor.set_motor_left(0.2)
                self.motor.set_motor_right(0.6)
                return False
            else:
                self.step_state = 2

        elif self.step_state == 2:
            # 元の進行方向へ復帰
            if current_yaw > 5.0:
                self.motor.set_motor_left(0.5)
                self.motor.set_motor_right(0.2)
                return False
            else:
                self.motor.stop()
                return True

        return False