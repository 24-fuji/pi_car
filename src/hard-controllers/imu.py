import time
from mpu6050 import mpu6050

# センサーの初期化（アドレス0x68）
sensor = mpu6050(0x68)

print("IMUデータの取得を開始します（1秒おき）...")
print("-" * 50)

try:
    while True:
        # データの取得
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        temp = sensor.get_temp()

        # 結果の出力
        print(f"Accel: x={accel_data['x']:.2f}, y={accel_data['y']:.2f}, z={accel_data['z']:.2f} (m/s^2)")
        print(f"Gyro:  x={gyro_data['x']:.2f}, y={gyro_data['y']:.2f}, z={gyro_data['z']:.2f} (deg/s)")
        print(f"Temp:  {temp:.1f} C")
        print("-" * 50)

        # 1秒待機
        time.sleep(1)

except KeyboardInterrupt:
    print("\n計測を終了しました。")