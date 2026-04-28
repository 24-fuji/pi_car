# pi_car

## 試行時は以下のハードウェアを使用。OSは間違えてraspberry pi 4(64bit)を採用
control cat using raspberry pi 3 model b+

```bash
cd <code_ws>/src
git clone git clone git clone git@github.com:24-fuji/pi_car.git
```

# ライブラリのインストール
sudo apt update
sudo apt install python3-gpiozero
sudo apt install python3-opencv
sudo apt install i2c-tools
i2cdetect -y 1