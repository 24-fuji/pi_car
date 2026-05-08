# pi_car

## 試行時は以下のハードウェアを使用。OSは間違えてraspberry pi 4(64bit)を採用
control cat using raspberry pi 3 model b+

```bash
cd <code_ws>/src
git clone git clone git clone git@github.com:24-fuji/pi_car.git
```

# ライブラリのインストール
```bash
sudo apt update
sudo apt install python3-gpiozero
sudo apt install python3-opencv
sudo apt install i2c-tools
sudo apt install -y python3-dbus
```
I2Cの配線が完了したかを調べられる
```bash
i2cdetect -y 1
```

# I2Cの有効化
```bash
sudo raspi-config
```
3 Insterfacing Optionsを選択
I2Cを選択
Would you like the ARM I2C interface to be enable?にYesを選択
<Ok> -> <Finish>
設定が反映されなければ再起動する

# bluetoothの初期設定
```bash
sudo rfkill unblock bluetooth
sudo bluetoothctl power on
```
2回目以降はファイルを起動し接続端末から接続するだけでよい
