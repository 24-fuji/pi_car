# teleop.py

class DifferentialDriveTeleop:
    def __init__(self, max_speed_ratio=1.0):
        self.max_speed_ratio = max_speed_ratio

    def twist_to_wheels(self, linear: float, angular: float):
        """
        linear (前後: -1.0 〜 1.0) と angular (旋回: -1.0 〜 1.0) 
        から左右モーターのデューティ比 (-1.0 〜 1.0) を算出する
        """
        # 差動二輪の簡易運動学計算
        left_speed = linear - angular
        right_speed = linear + angular

        # 最大値が1.0を超えた場合に全体の比率を維持したまま正規化（スケーリング）
        max_mag = max(abs(left_speed), abs(right_speed))
        if max_mag > 1.0:
            left_speed /= max_mag
            right_speed /= max_mag

        return left_speed * self.max_speed_ratio, right_speed * self.max_speed_ratio