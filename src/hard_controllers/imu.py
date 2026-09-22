import smbus2
import time
import math

class MPU6050:
    DEV_ADDR = 0x68
    PWR_MGMT_1 = 0x6B
    GYRO_ZOUT_H = 0x47

    def __init__(self, bus_num=1):
        self.bus = smbus2.SMBus(bus_num)
        # スリープ解除
        self.bus.write_byte_data(self.DEV_ADDR, self.PWR_MGMT_1, 0)
        
        self.yaw = 0.0
        self.last_time = time.time()
        self.gyro_z_offset = 0.0
        self.calibrate_gyro()

    def calibrate_gyro(self, samples=100):
        """静止状態でのオフセット除去（キャリブレーション）"""
        total = 0
        for _ in range(samples):
            total += self._read_raw_gyro_z()
            time.sleep(0.005)
        self.gyro_z_offset = total / samples

    def _read_raw_gyro_z(self):
        high = self.bus.read_byte_data(self.DEV_ADDR, self.GYRO_ZOUT_H)
        low = self.bus.read_byte_data(self.DEV_ADDR, self.GYRO_ZOUT_H + 1)
        val = (high << 8) + low
        if val >= 0x8000:
            val = -(65536 - val)
        return val / 131.0  # LSB/(deg/s) for ±250deg/s

    def update(self):
        """定期実行して Yaw角 を更新・積分"""
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        gyro_z = self._read_raw_gyro_z() - self.gyro_z_offset
        # ノイズの微小値をカット（不感帯設定）
        if abs(gyro_z) < 0.5:
            gyro_z = 0.0

        self.yaw += gyro_z * dt
        return self.yaw

    def get_yaw(self):
        return self.yaw

    def reset_yaw(self):
        self.yaw = 0.0
        self.last_time = time.time()