import cv2

# カメラの初期化 (0は通常1台目のカメラ)
# USBカメラが認識されない場合は 1, 2 と数字を変えてみてください
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("カメラが見つかりません")
    exit()

print("プレビューを開始します。'q'キーで終了します。")

while True:
    # フレームを1枚ずつ読み込む
    ret, frame = cap.read()

    if not ret:
        print("映像を取得できませんでした")
        break

    # ウィンドウに表示
    cv2.imshow('USB Camera Preview', frame)

    # 'q' キーが押されたらループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 後片付け
cap.release()
cv2.destroyAllWindows()

# 以下でコマンドラインから動確できる
# sudo apt update
# sudo apt install ffmpeg
# ffplay /dev/video0