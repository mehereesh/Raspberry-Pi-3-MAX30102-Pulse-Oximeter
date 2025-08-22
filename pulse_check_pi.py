import time
import numpy as np
from smbus2 import SMBus
from scipy.signal import find_peaks

# MAX30102 I2C address (default 0x57)
MAX30102_I2C_ADDR = 0x57

class MAX30102:
    def __init__(self, address=MAX30102_I2C_ADDR, bus=1):
        self.bus = SMBus(bus)
        self.address = address
        self.setup()

    def write_reg(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def read_fifo(self):
        try:
            # FIFO Register = 0x07
            data = self.bus.read_i2c_block_data(self.address, 0x07, 6)
            red_led = (data[0] << 16 | data[1] << 8 | data[2]) & 0x3FFFF
            ir_led = (data[3] << 16 | data[4] << 8 | data[5]) & 0x3FFFF
            return red_led, ir_led
        except OSError:
            return None, None

    def setup(self):
        # Reset
        self.write_reg(0x09, 0x40)
        time.sleep(0.1)

        # Interrupt config
        self.write_reg(0x02, 0xC0)  # A_FULL and PPG_RDY
        self.write_reg(0x03, 0x00)

        # FIFO config
        self.write_reg(0x08, 0x4F)

        # Mode config -> SpO2 mode
        self.write_reg(0x09, 0x03)

        # SpO2 config (411 Hz, 18-bit)
        self.write_reg(0x0A, 0x27)

        # LED pulse amplitude
        self.write_reg(0x0C, 0x24)  # Red LED
        self.write_reg(0x0D, 0x24)  # IR LED


def calculate_bpm(ir_data, fs=100):
    ir_array = np.array(ir_data)
    ir_array = ir_array - np.mean(ir_array)

    peaks, _ = find_peaks(ir_array, distance=fs*0.6)
    peak_times = np.diff(peaks) / fs

    if len(peak_times) > 0:
        bpm = 60.0 / np.mean(peak_times)
        return int(bpm)
    else:
        return 0


def main():
    sensor = MAX30102()
    ir_buffer = []
    bpm_list = []

    print("Place your finger on the sensor...")
    start_time = time.time()

    # Run only for 10 seconds
    while time.time() - start_time < 10:
        red, ir = sensor.read_fifo()
        if red is None or ir is None:
            continue

        ir_buffer.append(ir)

        # Process ~2 sec worth of data (200 samples @100Hz)
        if len(ir_buffer) > 200:
            bpm = calculate_bpm(ir_buffer[-200:])
            if bpm > 0:
                bpm_list.append(bpm)
                print(f"Instant Heart Rate: {bpm} BPM")
            ir_buffer = ir_buffer[-200:]

        time.sleep(0.01)  # ~100Hz sampling

    # After 10 seconds → print average
    if bpm_list:
        avg_bpm = int(np.mean(bpm_list))
        print("\n=================================")
        print(f" Your Pulse is {avg_bpm} BPM (average of 10s)")
        print("=================================\n")
    else:
        print("No valid pulse detected in 10s.")


if __name__ == "__main__":
    main()
