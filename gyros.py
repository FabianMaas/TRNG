import smbus
import math
import time

# MPU6050 Register Adressen
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# MPU6050 Geräteadresse
DEVICE_ADDRESS = 0x68

# Initialisierung des I2C-Bus
bus = smbus.SMBus(1)

# Initialisierung des MPU6050
def MPU_Init():
    bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)

# Funktion zum Lesen der Rohdaten des Sensors
def read_raw_data(addr):
    high = bus.read_byte_data(DEVICE_ADDRESS, addr)
    low = bus.read_byte_data(DEVICE_ADDRESS, addr + 1)
    value = (high << 8) | low

    # Umskalierung auf den Bereich von -32768 bis 32767
    if value > 32768:
        value = value - 65536
    return value

# Funktion zur Berechnung der Rotation in Grad
def get_rotation():
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_YOUT_H)
    accel_z = read_raw_data(ACCEL_ZOUT_H)

    x_rotation = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2))
    y_rotation = math.atan2(accel_x, math.sqrt(accel_y**2 + accel_z**2))

    # Konvertierung in Grad
    x_rotation = math.degrees(x_rotation)
    y_rotation = math.degrees(y_rotation)

    return x_rotation, y_rotation

# Hauptprogramm
if __name__ == "__main__":
    MPU_Init()

    try:
        while True:
            x_angle, y_angle = get_rotation()
            print("X rotation: ", x_angle)
            print("Y rotation: ", y_angle)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
