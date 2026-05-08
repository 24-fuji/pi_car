import subprocess
import time

def run_bt(cmd):
    # -p プロンプトなしで実行
    return subprocess.run(["bluetoothctl"] + cmd.split(), capture_output=True, text=True)

def setup_headless_bluetooth():
    print("--- ヘッドレス・ペアリングモード起動 ---")
    # 電源ONとロック解除
    subprocess.run(["sudo", "rfkill", "unblock", "bluetooth"])
    run_bt("power on")
    
    # ここが重要：エージェントの設定
    run_bt("agent NoInputNoOutput") # 確認画面を出さない設定
    run_bt("default-agent")
    run_bt("discoverable on")
    run_bt("pairable on")
    
    # 既存のペアリング要求を全て許可するバックグラウンド処理の代わり
    # 実際には bluetoothctl のエージェントが自動で yes を返してくれるようになります。
    print("準備完了。スマホから接続してください。ポップアップは出ないはずです。")

def main():
    setup_headless_bluetooth()
    
    try:
        while True:
            # 接続済みデバイスがあるかチェック
            res = run_bt("devices Paired")
            if res.stdout:
                # ペアリングされたデバイスを自動的に「信頼(trust)」状態にする
                # これをしないと次回接続時にまた確認が出る場合があります
                for line in res.stdout.strip().split('\n'):
                    mac = line.split()[1]
                    run_bt(f"trust {mac}")
                
                # 接続状態の確認
                info = run_bt("info")
                if "Connected: yes" in info.stdout:
                    print("\r[接続中] 制御可能です      ", end="")
                else:
                    print("\r[待機中] ペアリング受付中...", end="")
            
            time.sleep(2)
    except KeyboardInterrupt:
        run_bt("discoverable off")

if __name__ == "__main__":
    main()
