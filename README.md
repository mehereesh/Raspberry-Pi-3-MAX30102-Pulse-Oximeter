🩺 Raspberry Pi 3 + MAX30102 Pulse Oximeter (10-Second Test)

This project demonstrates how to interface a MAX30102 Pulse Oximeter & Heart Rate Sensor with a Raspberry Pi 3 (B/B+) running Python 3.12.
It captures heart rate (BPM) and blood oxygen saturation (SpO₂) values for 10 seconds and displays the results in the terminal.

📌 Features

✅ Reads real-time data from MAX30102 using I²C

✅ Displays Heart Rate (BPM) & SpO₂ (%)

✅ Runs for 10 seconds and auto-stops

✅ Python 3.12 compatible

✅ Lightweight & simple implementation

🛠️ Hardware Requirements

Raspberry Pi 3 (B/B+) with Raspberry Pi OS

MAX30102 Pulse Oximeter Sensor

Jumper wires & Breadboard

⚡ Circuit Connection (I²C)
MAX30102 Pin	Raspberry Pi Pin
VIN (3.3V)	Pin 1 (3.3V)
GND	Pin 6 (GND)
SCL	Pin 5 (GPIO3/SCL)
SDA	Pin 3 (GPIO2/SDA)
📦 Installation
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Enable I2C
sudo raspi-config  # -> Interfacing Options -> I2C -> Enable

# Install Python libraries
pip install smbus2 numpy

🚀 Run the Code
python3 max30102_test.py


The script will run for 10 seconds and print live Heart Rate & SpO₂ values.

📜 Example Output
Starting MAX30102 Pulse Oximeter Test...
Time: 0.00s | Heart Rate: 76 BPM | SpO₂: 98%
Time: 1.01s | Heart Rate: 77 BPM | SpO₂: 97%
Time: 2.02s | Heart Rate: 76 BPM | SpO₂: 98%
...
Test complete. Data collection stopped.

🔑 Keywords

Raspberry Pi 3 Pulse Oximeter MAX30102 Heart Rate SpO2 Python 3.12 I2C Biomedical Sensor IoT Healthcare Medical Devices Vital Signs Monitoring

📌 Notes

Make sure I²C is enabled on your Raspberry Pi.

This is a basic implementation for testing.

For medical use, always rely on certified devices.
