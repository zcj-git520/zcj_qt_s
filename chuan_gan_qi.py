#-*-coding:utf-8 -*-
"""
这是传感器模块：
传感器包括：超声波测距,以及陀螺仪测速度
"""
import RPi.GPIO as GPIO
import time
import setting
class Sensor():

    def __init__(self,TRIG,ECHO):
        self.TRIG = TRIG
        self.ECHO = ECHO
        self.ObstaclePin = setting.ObstaclePin

    def setup(self):
        GPIO.setmode(GPIO.BOARD)   #设置编号的的方式
        GPIO.setup(self.TRIG,GPIO.OUT)  #设置trig为输出的口
        GPIO.setup(self.ECHO,GPIO.IN)   #设置echo为输入的口
        GPIO.setup(self.ObstaclePin,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    def distance(self):
        GPIO.output(self.TRIG,0)  #设置输出的电压为低电压
        time.sleep(0.00002)              #设置延时
        GPIO.output(self.TRIG,1) #设置输出的电压为高电压
        time.sleep(0.00001)
        GPIO.output(self.TRIG,0)
        while GPIO.input(self.ECHO) == 0:
            pass
        time1 = time.time()
        while GPIO.input(self.ECHO) == 1:
            pass
        time2 = time.time()
        during = time2 - time1
        return during * 340 / 2 * 100
    def back_redline(self):
        if 0 ==  GPIO.input(self.ObstaclePin):
            return 1
        else:
            return 0
    def destroy(self):
        GPIO.cleanup()



