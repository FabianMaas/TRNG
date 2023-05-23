import smbus            
from time import sleep        
import math
import RPi.GPIO as GPIO
import sys


class Gyroscope:

    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_ENABLE   = 0x38
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47
    Device_Address = 0x68  
    bus = smbus.SMBus(1)
    
    
    def MPU_Init(self):
        self.bus.write_byte_data(self.Device_Address, self.SMPLRT_DIV, 79)
        self.bus.write_byte_data(self.Device_Address, self.PWR_MGMT_1, 1)
        self.bus.write_byte_data(self.Device_Address, self.CONFIG, 0)
        self.bus.write_byte_data(self.Device_Address, self.GYRO_CONFIG, 24) 
        self.bus.write_byte_data(self.Device_Address, self.Device_Address, self.INT_ENABLE, 1)
    
    
    def read_raw_data(self, addr):
            high = self.bus.read_byte_data(self.Device_Address, addr)
            low = self.bus.read_byte_data(self.Device_Address, addr+1)
            value = ((high << 8) | low)
            if(value > 32768):
                    value = value - 65536
            return value
    

    def dist(a, b):
        return math.sqrt((a*a) + (b*b))
    
    def get_y_rotation(x, y, z):
        radians = math.atan2(y, z)
        return -(radians * (180.0 / math.pi))
    
    def get_x_rotation(x, y, z):
        radians = math.atan2(x, math.dist(y, z))
        return -(radians * (180.0 / math.pi))
    
    
    def get_angles(self):
        try:
            self.MPU_Init()
            acc_x = self.read_raw_data(self.ACCEL_XOUT_H)
            acc_y = self.read_raw_data(self.ACCEL_YOUT_H)
            acc_z = self.read_raw_data(self.ACCEL_ZOUT_H)
            
            acclX_scaled = acc_x * .000061 * 9.80665
            acclY_scaled = acc_y * .000061 * 9.80665
            acclZ_scaled = acc_z * .000061 * 9.80665
            
            x_angle = round(self.get_x_rotation(acclX_scaled, acclY_scaled, acclZ_scaled),0)
            y_angle = round(self.get_y_rotation(acclX_scaled, acclY_scaled, acclZ_scaled),0)
            print("X rotation: ", x_angle)
            print("Y rotation: ",y_angle)
            
            angle_map = {
                "x_angle": "{x_angle}",
                "y_angle": "{y_angle}",
            }
            
        except Exception as e:
            print(e)
            
        return angle_map