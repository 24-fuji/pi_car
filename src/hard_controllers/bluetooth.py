import subprocess
import time
import os

def run_bt(cmd):
    """bluetoothctlコマンドを実行"""
    subprocess.run(["bluetoothctl"] + cmd.split(), capture_output=True, text=True)

def is_connected():
    """デバイスが接続されているかチェック"""
    res = subprocess.run(["bluetoothctl", "devices", "Paired"], capture_output=True, text=True)
    # ペアリング済みデバイスの一覧を取得
    paired_devices = res.stdout.strip().split('\n')
    
    for dev in paired_devices:
        if not dev: continue
        mac = dev.split()[1]
        # そのデバイスの現在の情報を取得
        info = subprocess.run(["bluetoothctl", "info", mac], capture_output=True, text=True).stdout
        if "Connected: yes" in info:
            return True, dev
    return False, None

def main():
    print("=== Bluetooth 接続監視エンジン ===")
    
    # Bluetoothを「見つけられる状態」にする
    run_bt("power on")
    run_bt("discoverable on")
    run_bt("pairable on")
    
    # 自分の名前を確認
    name_res = subprocess.run(["hostname"], capture_output=True, text=True)
    print(f"デバイス名: {name_res.stdout.strip()} (スマホ等でこの名前を探してください)")
    print("ペアリング待機中...")

    try:
        while True:
            connected, dev_info = is_connected()
            if connected:
                print(f"\n[接続済み] {dev_info}")
                # 接続されたら発見モードをオフにして負荷を減らす
                run_bt("discoverable off")
            else:
                print(".", end="", flush=True)
            
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n終了します")
        run_bt("discoverable off")

if __name__ == "__main__":
    main()
