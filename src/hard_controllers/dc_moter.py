# dc_motor_controller.py
from gpiozero import OutputDevice, PWMOutputDevice

class DRV8835DualMotor:
    def __init__(self, a_phase_pin=5, a_enbl_pin=12, b_phase_pin=6, b_enbl_pin=13):
        # 左モーター (Motor A)
        self.a_phase = OutputDevice(a_phase_pin)
        self.a_enbl = PWMOutputDevice(a_enbl_pin, frequency=20000)

        # 右モーター (Motor B)
        self.b_phase = OutputDevice(b_phase_pin)
        self.b_enbl = PWMOutputDevice(b_enbl_pin, frequency=20000)

        self.stop()

    def set_motor_left(self, command_val: float):
        """左モーター制御 (command_val: -1.0 ～ 1.0)"""
        val = max(-1.0, min(1.0, command_val))
        if val > 0:
            self.a_phase.off()       # 正転
            self.a_enbl.value = val
        elif val < 0:
            self.a_phase.on()        # 逆転
            self.a_enbl.value = abs(val)
        else:
            self.a_enbl.value = 0

    def set_motor_right(self, command_val: float):
        """右モーター制御 (command_val: -1.0 ～ 1.0)"""
        val = max(-1.0, min(1.0, command_val))
        if val > 0:
            self.b_phase.off()       # 正転
            self.b_enbl.value = val
        elif val < 0:
            self.b_phase.on()        # 逆転
            self.b_enbl.value = abs(val)
        else:
            self.b_enbl.value = 0

    def stop(self):
        self.a_enbl.value = 0
        self.b_enbl.value = 0
        self.a_phase.off()
        self.b_phase.off()

    def close(self):
        self.stop()
        self.a_enbl.close()
        self.a_phase.close()
        self.b_enbl.close()
        self.b_phase.close()