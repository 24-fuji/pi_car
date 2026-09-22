import json
import ssl
import time
import threading
import sys
import os

# プロジェクトルート（pi_car）の src ディレクトリを Python の検索パスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# ディレクトリ構造に合わせてインポート
from hard_controllers.dc_moter import DRV8835DualMotor  # hard_controllers 内の dc_moter.py から読み込み
from soft_controllers.tereop import DifferentialDriveTeleop  # ファイル名 tereop.py に合わせる

# --- HiveMQ 接続設定 ---
MQTT_BROKER = "dfc5778a265a49aa9e800f7cdcd750c0.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "24fuji"
MQTT_PASS = "taiyakiyaketa"

# Webアプリのデフォルト設定に合わせてトピックを変更
MQTT_TOPIC = "robot/teleop"

# タイムアウト時間（秒） - この時間以上データ更新がなければ非常停止
TIMEOUT_SEC = 0.5

# インスタンス化
motor_driver = DRV8835DualMotor()
teleop = DifferentialDriveTeleop()

# 最終受信時刻の管理
last_msg_time = time.time()
running = True

def timeout_checker():
    """一定時間メッセージが届かない場合に自動で停止させる安全スレッド"""
    global last_msg_time, running
    while running:
        if time.time() - last_msg_time > TIMEOUT_SEC:
            # タイムアウト発生時は安全のために停止
            motor_driver.stop()
        time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"HiveMQに接続成功。トピック [{MQTT_TOPIC}] を購読します。")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"接続失敗 エラーコード: {rc}")

def on_message(client, userdata, msg):
    """
    WebUIからのJSONペイロード受信処理
    """
    global last_msg_time
    last_msg_time = time.time()

    try:
        data = json.loads(msg.payload.decode('utf-8'))
        
        # 左スティックの値を取得 (x: 左右, y: 前後)
        left_stick = data.get("left_stick", {"x": 0.0, "y": 0.0})
        
        # y: 前後 ( -1.0 〜 1.0 )
        # x: 旋回 ( -1.0 〜 1.0 )
        linear = float(left_stick.get("y", 0.0))
        angular = float(left_stick.get("x", 0.0))

        # 差動二輪運動モデルで左右のモーター制御値(-1.0 〜 1.0)に変換
        left_val, right_val = teleop.twist_to_wheels(linear, angular)

        # モータードライバーへ即時反映 (FF制御)
        motor_driver.set_motor_left(left_val)
        motor_driver.set_motor_right(right_val)

        print(f"\r[受信] Joy L(x:{angular:+.2f}, y:{linear:+.2f}) -> Motor Out [L:{left_val:+.2f}, R:{right_val:+.2f}]", end="")

    except json.JSONDecodeError:
        print("\nJSONデータパースエラー")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")

def main():
    global running
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASS)

    # TLS 暗号化設定
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

    client.on_connect = on_connect
    client.on_message = on_message

    # タイムアウト監視スレッドの開始
    t = threading.Thread(target=timeout_checker, daemon=True)
    t.start()

    print(f"HiveMQ サーバー ({MQTT_BROKER}) へ接続中...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nプログラムを停止します...")
    finally:
        running = False
        motor_driver.stop()
        motor_driver.close()
        client.disconnect()
        print("停止完了")

if __name__ == "__main__":
    main()