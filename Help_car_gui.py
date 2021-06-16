"""
智能辅助驾驶系统的GUI界面
"""
from PyQt5.QtWidgets import QWidget,QToolButton,QApplication,QLabel,QMessageBox,QPushButton,QMainWindow,QAction,QToolBar
from PyQt5.QtCore import Qt,QSize,QUrl,QTimer,QDateTime,QThread
from PyQt5.QtGui import  QIcon,QDesktopServices,QFont,QPalette,QColor,QBrush,QPixmap,QImage
import sys,time
import threading
import io
import socket
import struct
import time
import cv2
import numpy as np
from urllib import request
from bs4 import BeautifulSoup
import cv2

#import voice_re
import os
# from PyQt5.QtWebEngineWidgets import *
#from PyQt5.QtWebKitWidgets import *
#import chuan_gan_qi
#import picamera
import setting

place = setting.place
city_codes = setting.city_codes
image_path = setting.image_path
weather_imagepath = setting.weather_imagepath
ip = setting.ip
port = setting.port

DETE_DATA = []             #图像识别数据
video_lable = ''           #显示图像的全局框
tame =''                   #显示时间
class Weather_data():
    def __init__(self):
        self.city_codes = city_codes
    def  get_url(self,city):
        url = 'http://www.weather.com.cn/weather1d/' + city_codes[city] + '.shtml'
        return url
    def get_html(self,city):
        req = request.urlopen(self.get_url(city))
        html = req.read().decode('utf-8')
        return html
    def get_data(self,city):
        weather = {}
        soup = BeautifulSoup(self.get_html(city), 'lxml')
        weather['day_wea'] = soup.select('div.t > ul.clearfix > li > p.wea')[0].text
        weather['night_wea'] = soup.select('div.t > ul.clearfix > li > p.wea')[1].text
        weather['day_tem'] = soup.select('div.t > ul.clearfix > li > p.tem > span')[0].text
        weather['night_tem'] = soup.select('div.t > ul.clearfix > li > p.tem > span')[1].text
        return weather
#基础界面
class BaseWindow(QWidget):
    def __init__(self):
        super(BaseWindow, self).__init__()
        self.setWindowTitle("吉吉车载系统")
        self.palete = QPalette()
        # self.palete.setColor(self.backgroundRole(),QColor(QColor("black")))
        self.palete.setBrush(self.backgroundRole(), QBrush(QPixmap(image_path+"/backgrond.jpg")))
        self.setPalette(self.palete)
        """
        设置窗口的属性：Qt.FramelessWindowHint:没有边框的窗口  
                        Qt.WindowStaysOnTopHint:总在上面的窗口
                        Qt.CustomizeWindowHint :自定义窗口标题栏
                        Qt.WindowTitleHint :显示窗口标题栏
                        Qt.WindowSystemMenuHint :显示系统菜单
                        Qt.Drawer :去掉窗口左上角的图标
        """
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setWindowModality(Qt.WindowModal)
        self.setGeometry(0, 3, 800, 480)
        # self.setGeometry(200, 200, 800, 480)
#主界面
class MainWindow(BaseWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.function()
        # self.weather()
    def Show_Weather(self):

        self.day_img_label = QLabel(self)
        self.night_img_label = QLabel(self)
        self.day_title = QLabel('白天',self)
        self.night_title = QLabel('夜间',self)
        self.day_weather = QLabel(self)
        self.night_weather =QLabel(self)
        self.day_title.move(530,80)
        self.night_title.move(690,80)
        self.day_img_label.move(480,120)
        self.night_img_label.move(640,120)
        self.day_weather.move(520,200)
        self.night_weather.move(680,200)
        self.day_img_label.resize(150,80)
        self.night_img_label.resize(150,80)
        self.day_weather.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:20px;font-weight:bold;font-family:宋体;}")
        self.night_weather.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:20px;font-weight:bold;font-family:宋体;}")
        self.night_title.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:20px;font-weight:bold;font-family:宋体;}")
        self.day_title.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:20px;font-weight:bold;font-family:宋体;}")
        try:
            threading.Thread(self.Update())
        except:
            pass
    def __get_images__(self, wea_str):

        imags = {"day_小雨": weather_imagepath+'/light_rain.png', "night_小雨": weather_imagepath+"/hail.png",
                 "day_多云": weather_imagepath+'/fog.png', "night_多云": weather_imagepath+"/fog_night.png",
                 "day_晴": weather_imagepath+'/cloudy1.png', "night_晴": weather_imagepath+"/cloudy1_night.png",
                 "day_阴": weather_imagepath+'/cloudy5.png', "night_阴": weather_imagepath+"/cloudy4_night.png",
                 }
        return imags[wea_str]
    def Update(self):
        wea = Weather_data()
        weather_data = wea.get_data(place)
        pixmap_day = QPixmap(self.__get_images__('day_' + weather_data['day_wea']))
        self.day_img_label.setPixmap(pixmap_day)
        self.day_img_label.setScaledContents(True)
        pixmap_night = QPixmap(self.__get_images__('day_' + weather_data['night_wea']))
        self.night_img_label.setPixmap(pixmap_night)
        self.night_img_label.setScaledContents(True)
        self.day_weather.setText(str(weather_data['day_wea'] + weather_data['day_tem'] + '℃'))
        self.night_weather.setText(str(weather_data['night_wea'] + weather_data['night_tem'] + '℃'))
    def  ShowTime(self):
        lable = QLabel(self)
        lable.resize(400, 100)
        lable.move(50, 120)
        lable.setStyleSheet("QLabel{border: 2px solid blue;}" )
        lable_img = QLabel(self)
        lable_img.resize(30, 20)
        lable_img.move(150, 90)
        pixmap = QPixmap(image_path+'/dinwei.png')
        lable_img.setPixmap(pixmap)
        lable_img.setScaledContents(True)
        self.place_lable = QLabel(place,self)
        self.place_lable.resize(200, 100)
        self.place_lable.move(200, 50)
        # self.place_lable.setAlignment(Qt.AlignCenter)
        self.place_lable.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:30px;font-weight:bold;font-family:宋体;}")
        self.time_lable = QLabel(self)
        self.time_lable.resize(200,100)
        self.time_lable.move(20, 120)
        self.time_lable.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:50px;font-weight:bold;font-family:宋体;}")
        self.data_lable = QLabel(self)
        self.data_lable.resize(230, 100)
        self.data_lable.move(220,120)
        self.time_lable.setAlignment(Qt.AlignCenter)
        self.data_lable.setAlignment(Qt.AlignCenter)
        self.data_lable.setWordWrap(True)
        self.data_lable.setStyleSheet(
            "QLabel{}" "QLabel{color:white;font-size:30px;font-weight:bold;font-family:宋体;}")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showtime)
        self.timer.start()
    def showtime(self):
        global tame
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        time = text[8:-8]
        week = text[:2]
        data = text[-4:]+'年'+ text[3:5]+ text[6:8]+'日'
        if tame != time:
            tame = time
        self.time_lable.setText(tame)
        self.data_lable.setText(data+week)
    def function(self):
        self.system_setup = QToolButton(self)  # 工具按钮得实例化
        self.system_setup.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.system_setup.setText("系统控制")  # 设置文字
        self.system_setup.setFont(QFont("宋体", 15))
        self.system_setup.setIcon(QIcon(image_path+"/system_setup.png"))  # 设置图标
        self.system_setup.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.system_setup.setStyleSheet("color:white;border: 2px solid blue;border-radius:40")
        self.system_setup.move(60, 270)  # 按钮的位置
        self.system_setup.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.system_setup.clicked.connect(self.jump_system_setup)

        self.tb_menu = QToolButton(self)
        self.tb_menu.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_menu.setText("菜单应用")  # 设置文字
        self.tb_menu.setFont(QFont("宋体", 15))
        self.tb_menu.setIcon(QIcon(image_path+"/menu.png"))  # 设置图标
        self.tb_menu.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_menu.setStyleSheet("color:white;border: 2px solid blue;border-radius:40")
        self.tb_menu.move(320, 270)  # 按钮的位置
        self.tb_menu.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_menu.clicked.connect(self.jump_menu)

        self.tb_language_interaction = QToolButton(self)
        self.tb_language_interaction .setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_language_interaction .setText("语音交互")  # 设置文字
        self.tb_language_interaction .setFont(QFont("宋体", 15))
        self.tb_language_interaction .setIcon(QIcon(image_path+"/tb_language_interaction.png"))  # 设置图标
        self.tb_language_interaction .setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_language_interaction .setStyleSheet("color:white;border: 2px solid blue;border-radius:40")
        self.tb_language_interaction .move(580, 270)  # 按钮的位置
        self.tb_language_interaction .setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_language_interaction.clicked.connect(self.jump_language_interaction)

        self.Show_Weather()
        self.ShowTime()
        self.show()
    def jump_menu(self):
        self.function = FunctionWindow()
        self.hide()
    def jump_language_interaction(self):
        QMessageBox.information(self,"温馨提示","语音交互已经开启")
        threading.Thread(target=self.speak_voice).start()
    def speak_voice(self):
        # 录音
        filename = setting.filename  # 录音临时音频文件
        wea = Weather_data()
        weather_data = wea.get_data(place)
        text = '汽车技术数据可以全面反映汽车的外观和外形尺寸、汽车的性能指标、软硬件配置等。技术数据是购车人选择汽车时关注的焦点，也是汽车用户在用车过程中经常翻阅的技术资料。通过正确解读汽车技术数据，可以分析比较不同汽车的优劣，有利于选择适宜的汽车，也有利于更好地使用汽车，最大限度地发挥其性能。'
        voice_re.speak(text, 32)
        def continue_recodervoice():
            r = voice_re.recoder_voice()
            r.redecor()
            r.savewav(filename)
            data = voice_re._recognition(filename)
            return data
        while True:
            data = continue_recodervoice()
            while  "小白兔，" in data:
                try:
                    voice_re.play_systeam()
                    data = continue_recodervoice()
                    # if "关闭" in data:
                    #     sys.exit()
                    if "加速" in data:
                        text = '收到，正在加速'
                        voice_re.speak(text,2)
                        break
                    if "减速" in data:
                        text = '收到，正在减速'
                        voice_re.speak(text, 2)
                        break
                    if "左转" in data:
                        text = '收到，正在左转'
                        voice_re.speak(text,2)
                        break
                    if '天气' in data:
                        wea = Weather_data()
                        weather1 = wea.get_data(place)
                        text = place +"白天"+str(weather1['day_wea'])+str(weather1[ 'day_tem'])+'摄氏度'+"晚上"+str(weather1['night_wea'])+str(weather1[ 'night_tem'])+'摄氏度'
                        print(weather1)
                        voice_re.speak(text, 10)
                        break
                    if '查看数据' in data:
                        text = '汽车技术数据可以全面反映汽车的外观和外形尺寸、汽车的性能指标、软硬件配置等。技术数据是购车人选择汽车时关注的焦点，也是汽车用户在用车过程中经常翻阅的技术资料。通过正确解读汽车技术数据，可以分析比较不同汽车的优劣，有利于选择适宜的汽车，也有利于更好地使用汽车，最大限度地发挥其性能。'
                        voice_re.speak(text,32 )
                        break
                except:
                    pass

    def jump_system_setup(self):
        self.a = operation_car()
        self.hide()
#主功能界面呢
class operation_car(BaseWindow):
    def __init__(self):
        super(operation_car, self).__init__()
        self.tb_back_home = QToolButton(self)
        self.tb_back_home.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back_home.setIcon(QIcon(image_path + '/tb_back_home.png'))
        self.tb_back_home.setIconSize(QSize(50, 50))
        self.tb_back_home.setAutoRaise(True)
        self.tb_back_home.move(30, 10)
        self.tb_back_home.clicked.connect(self.jump_tb_back_home)

        self.tb_back = QToolButton(self)
        self.tb_back.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back.setIcon(QIcon(image_path + '/tb_back.png'))
        self.tb_back.setIconSize(QSize(50, 50))
        self.tb_back.setAutoRaise(True)
        self.tb_back.move(700, 10)
        self.tb_back.clicked.connect(self.jump_tb_back)
        self.opeartion()
    def opeartion(self):
        self.lable = QLabel(self)
        self.lable.resize(200, 300)
        self.lable.move(150, 80)
        self.lable.setFont(QFont('宋体', 25))
        self.lable.setStyleSheet("color:white;border: 2px solid blue;border: 2px solid blue")
        self.Timer = QTimer(self)
        self.Timer.timeout.connect(self.show_lable)
        self.Timer.start(10)
        self.show()
    def show_lable(self):
        s1 = chuan_gan_qi.Sensor(setting.TRIG1,setting.ECHO1)
        s2 = chuan_gan_qi.Sensor(setting.TRIG2, setting.ECHO2)
        s3 = chuan_gan_qi.Sensor(setting.TRIG3, setting.ECHO3)
        try:

            s1.setup()
            s2.setup()
            s3.setup()
            data1 = s1.distance()
            data1 = round(data1, 2)
            data2 = s2.distance()
            data2 = round(data2, 2)
            data3 = s3.distance()
            data3 = round(data3, 2)
            self.lable.setText('前'+str(data1)+'cm'+'\n'+'左'+str(data2)+'cm'+'\n'+'右'+str(data3)+'cm')
            if 12.0 > data1:
                text = '注意，你离你前面的车只有'+str(data1)+'cm'
                voice_re.speak(text,5)

        finally:
            s1.destroy()
            s2.destroy()
            s3.destroy()


    def jump_tb_back_home(self):
        self.Timer.stop()
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.Timer.stop()
        self.fction = MainWindow()
        self.hide()
class FunctionWindow(BaseWindow):
    def __init__(self):
        super(FunctionWindow, self).__init__()
        self.initUI()
    def initUI(self):

        # 工具按钮得的属性，Qt.ToolButtonIconOnly (只显示图标) Qt.ToolButtonTextOnly(只显示文字)
        # Qt.ToolButtonTextBesideIcon(文字出现在图标的旁边) Qt.ToolButtonTextUnderIcon(文字出现在
        # 图标的下方)
        self.tb_back_home = QToolButton(self)
        self.tb_back_home.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back_home.setIcon(QIcon(image_path+'/tb_back_home.png'))
        self.tb_back_home.setIconSize(QSize(50,50))
        self.tb_back_home.setAutoRaise(True)
        self.tb_back_home.move(30,10)
        self.tb_back_home.clicked.connect(self.jump_tb_back_home)

        self.tb_back = QToolButton(self)
        self.tb_back.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back.setIcon(QIcon(image_path+'/tb_back.png'))
        self.tb_back.setIconSize(QSize(50, 50))
        self.tb_back.setAutoRaise(True)
        self.tb_back.move(700, 10)
        self.tb_back.clicked.connect(self.jump_tb_back)


        self.tb_map = QToolButton(self)  # 工具按钮得实例化
        self.tb_map.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_map.setText("导航")    #设置文字
        self.tb_map.setFont(QFont("宋体",15))
        self.tb_map.setIcon(QIcon(image_path+"/map.png"))  #设置图标
        self.tb_map.setIconSize(QSize(150,150))  #设置图标的大小
        self.tb_map.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_map.move(10,280)            #按钮的位置
        self.tb_map.setAutoRaise(True)   #属性是否保持启动自动升起
        self.tb_map.clicked.connect(self.open_map)

        self.tb_music = QToolButton(self)
        self.tb_music.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_music.setText("音乐")  # 设置文字
        self.tb_music.setFont(QFont("宋体",15))
        self.tb_music.setIcon(QIcon(image_path+"/yinyue.png"))  # 设置图标
        self.tb_music.setIconSize(QSize(150,150))  # 设置图标的大小
        self.tb_music.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_music.move(400, 280)  # 按钮的位置
        self.tb_music.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_music.clicked.connect(self.open_music)

        self.tb_car_record = QToolButton(self)
        self.tb_car_record.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_car_record.setText("行车记录")  # 设置文字
        self.tb_car_record.setFont(QFont("宋体", 15))
        self.tb_car_record.setIcon(QIcon(image_path+"/tb_car_record.png"))  # 设置图标
        self.tb_car_record.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_car_record.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_car_record.move(200, 280)  # 按钮的位置
        self.tb_car_record.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_car_record.clicked.connect(self.jamp_car_record)

        self.tb_photo = QToolButton(self)
        self.tb_photo.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_photo.setText("电话")  # 设置文字
        self.tb_photo.setFont(QFont("宋体", 15))
        self.tb_photo.setIcon(QIcon(image_path+"/phone.png"))  # 设置图标
        self.tb_photo.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_photo.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_photo.move(10, 80)  # 按钮的位置
        self.tb_photo.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_photo.clicked.connect(self.jump_photo)

        self.tb_bluetooth = QToolButton(self)
        self.tb_bluetooth.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_bluetooth.setText("蓝牙")  # 设置文字
        self.tb_bluetooth.setFont(QFont("宋体", 15))
        self.tb_bluetooth.setIcon(QIcon(image_path+"/tb_bluetooth.png"))  # 设置图标
        self.tb_bluetooth.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_bluetooth.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_bluetooth.move(200, 80)  # 按钮的位置
        self.tb_bluetooth.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_bluetooth.clicked.connect(self.jump_bluetooth)

        self.tb_radio = QToolButton(self)
        self.tb_radio.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_radio.setText("收音机")  # 设置文字
        self.tb_radio.setFont(QFont("宋体", 15))
        self.tb_radio.setIcon(QIcon(image_path+"/tb_radio.png"))  # 设置图标
        self.tb_radio.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_radio.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_radio.move(400, 80)  # 按钮的位置
        self.tb_radio.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_radio.clicked.connect(self.jamp_radio)

        self.tb_information= QToolButton(self)
        self.tb_information.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_information.setText("聊天工具")  # 设置文字
        self.tb_information.setFont(QFont("宋体", 15))
        self.tb_information.setIcon(QIcon(image_path+"/information.png"))  # 设置图标
        self.tb_information.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_information.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_information.move(600, 80)  # 按钮的位置
        self.tb_information.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_information.clicked.connect(self.jump_information)

        self.tb_car = QToolButton(self)
        self.tb_car.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_car.setText("车辆信息")  # 设置文字
        self.tb_car.setFont(QFont("宋体", 15))
        self.tb_car.setIcon(QIcon(image_path+"/car_d.png"))  # 设置图标
        self.tb_car.setIconSize(QSize(150, 150))  # 设置图标的大小
        self.tb_car.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_car.move(600, 280)  # 按钮的位置
        self.tb_car.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_car.clicked.connect(self.jump_carshow)
        self.show()
    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()
    def jump_tb_back(self):
        self.mainwindow = MainWindow()
        self.hide()
    def open_map(self):
        self.a = show_map()
        self.hide()
    def open_music(self):
        self.a = OpenMusic()
        self.hide()
    def jamp_car_record(self):
        self.a = show_drive_record()
        self.hide()
    def jump_photo(self):
        QMessageBox.information(self, "温馨提示", "正在开发，请稍后")
    def jump_bluetooth(self):
        QMessageBox.information(self, "温馨提示", "正在开发，请稍后")
    def jump_information(self):
        self.information = Show_information()
        self.hide()
    def jamp_radio(self):
        QMessageBox.information(self, "温馨提示", "正在开发，请稍后")
    def jump_carshow(self):
        self.a = Car_information()
        self.hide()
class show_map(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('地图导航')
        self.setGeometry(0, 10, 800, 480)
        navigation_bar = QToolBar()
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(50, 50))
        self.addToolBar(navigation_bar)

        self.tb_back_home = QAction(QIcon(image_path + '/tb_back_home.png'), '返回', self)
        self.tb_back = QAction(QIcon(image_path + '/tb_back.png'), '返回', self)
        navigation_bar.addAction(self.tb_back_home)
        navigation_bar.addAction(self.tb_back)
        self.tb_back_home.triggered.connect(self.jump_tb_back_home)
        self.tb_back.triggered.connect(self.jump_tb_back)
        self.browser = QWebView()
        #self.browser = QWebEngineView()
        self.browser.load(QUrl.fromLocalFile(setting.html))
        self.setCentralWidget(self.browser)
        self.show()
    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()
    def jump_tb_back(self):
        self.fction = FunctionWindow()
        self.hide()
class OpenMusic(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('QQ音乐')
        self.setGeometry(0, 10, 800, 480)
        navigation_bar = QToolBar()
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(50, 50))
        self.addToolBar(navigation_bar)

        self.tb_back_home = QAction(QIcon(image_path + '/tb_back_home.png'), '返回', self)
        self.tb_back = QAction(QIcon(image_path + '/tb_back.png'), '返回', self)
        navigation_bar.addAction(self.tb_back_home)
        navigation_bar.addAction(self.tb_back)
        self.tb_back_home.triggered.connect(self.jump_tb_back_home)
        self.tb_back.triggered.connect(self.jump_tb_back)
        self.browser = QWebView()
        # self.browser = QWebEngineView()
        self.browser.load(QUrl('https://y.qq.com/'))
        self.setCentralWidget(self.browser)
        self.show()
    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.fction = FunctionWindow()
        self.hide()
class show_drive_record(BaseWindow):
    def __init__(self):
        super(show_drive_record, self).__init__()
        self.tb_back_home = QToolButton(self)
        self.tb_back_home.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back_home.setIcon(QIcon(image_path + '/tb_back_home.png'))
        self.tb_back_home.setIconSize(QSize(50, 50))
        self.tb_back_home.setAutoRaise(True)
        self.tb_back_home.move(30, 10)
        self.tb_back_home.clicked.connect(self.jump_tb_back_home)

        self.tb_back = QToolButton(self)
        self.tb_back.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back.setIcon(QIcon(image_path + '/tb_back.png'))
        self.tb_back.setIconSize(QSize(50, 50))
        self.tb_back.setAutoRaise(True)
        self.tb_back.move(700, 10)
        self.tb_back.clicked.connect(self.jump_tb_back)
        self.show_drive()
    def show_drive(self):
        threading.Thread(target= self.show_camera).start()

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('1out.avi',self.fourcc,20.0,(640,480))

        global video_lable
        video_lable = QLabel(self)
        video_lable.resize(620,380)
        video_lable.move(150,80)
        video_lable.setStyleSheet("border: 2px solid blue")

        self.save_video_button = QPushButton('开始保存',self)
        self.save_video_button.move(10,150)
        self.save_video_button.setFont(QFont('宋体',25))
        self.save_video_button.setStyleSheet("color:white;border: 2px solid blue")
        self.save_video_button.clicked.connect(self.save_video)

        self.stop_button = QPushButton('停止保存', self)
        self.stop_button.move(10, 300)
        self.stop_button.setFont(QFont('宋体', 25))
        self.stop_button.setStyleSheet("color:white;border: 2px solid blue")
        self.stop_button.clicked.connect(self.stop_video)

        self.show()

    def show_camera(self,):
        global DETE_DATA
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP的模式进行
        client_socket.connect((ip, port))  # 连接服器
        connection = client_socket.makefile('wb')  # 创建二进制文件
        start = time.time()
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (416, 416)  # 图片的像数
                camera.framerate = 15  # 15 帧帲 帧/秒
                time.sleep(2)  # give 2 secs for camera to initilize
                stream = io.BytesIO()  # 创建字节流
                threading.Thread(target=self.show_photo_inPI, name="得到数据", args=(client_socket,)).start()
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                    # 将数据写进流中
                    try:
                        connection.write(struct.pack('<L', stream.tell()))
                        connection.flush()
                        self.data = np.fromstring(stream.getvalue(), dtype=np.uint8)
                        # 通过opencv解码numpy
                        self.img = cv2.imdecode(self.data, 1)
                        self.img = self.cvDrawBoxes(DETE_DATA,self.img)
                        show_1 = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
                        image = QImage(show_1.data, show_1.shape[1], show_1.shape[0], QImage.Format_RGB888)
                        video_lable.setPixmap(QPixmap.fromImage(image))
                        video_lable.setScaledContents(True)
                        stream.seek(0)
                        # 将数据流的指针指向起始位置
                        connection.write(stream.read())
                        if time.time() - start > 600:
                            break
                        # 重置捕获流，等待下一次捕获图像
                        stream.seek(0)
                        stream.truncate()
                    except:
                        pass
                connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
            client_socket.close()

    def show_photo_inPI(self,client_socket):
        global DETE_DATA
        while True:

            data = client_socket.recv(1024)
            detection_res = str(data, encoding="utf-8")
            detection_res = detection_res.split(',')
            detections = []
            for p in range(int(len(detection_res) / 6)):
                try:
                    temp1 = (
                        detection_res[0 + p * 6][4:-1],
                        float(detection_res[1 + p * 6]),
                        (float(detection_res[2 + p * 6].replace('(', '')), float(detection_res[3 + p * 6]),
                         float(detection_res[4 + p * 6]),
                         float(detection_res[5 + p * 6].replace(')', '').replace(']', ''))))
                    detections.append(temp1)
                except ValueError:
                    pass

            DETE_DATA = detections

    def convertBack(self,x, y, w, h):
        xmin = int(round(x - (w / 2)))
        xmax = int(round(x + (w / 2)))
        ymin = int(round(y - (h / 2)))
        ymax = int(round(y + (h / 2)))
        return xmin, ymin, xmax, ymax

    def cvDrawBoxes(self,detections, img):
        for detection in detections:
            x, y, w, h = detection[2][0], \
                         detection[2][1], \
                         detection[2][2], \
                         detection[2][3]
            xmin, ymin, xmax, ymax = self.convertBack(
                float(x), float(y), float(w), float(h))
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
            cv2.putText(img,
                        detection[0] +
                        " [" + str(round(detection[1] * 100, 2)) + "]",
                        (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        [0, 255, 0], 2)
        return img
    def jump_tb_back_home(self):
        self.out.release()
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.out.release()
        self.fction = FunctionWindow()
        self.hide()
    def save_video(self):
        self.timer_ = QTimer()
        self.timer_.timeout.connect(self.save_camera)
        self.timer_.start(10)

    def save_camera(self):
        self.img = cv2.imdecode(self.data, 1)
        self.out.write(self.img)
        self.timer_.start(10)
    def stop_video(self):
        self.timer_.stop()
        self.out.release()
class Show_information(BaseWindow):
    def __init__(self):
        super(Show_information, self).__init__()
        self.tb_back_home = QToolButton(self)
        self.tb_back_home.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back_home.setIcon(QIcon(image_path+'/tb_back_home.png'))
        self.tb_back_home.setIconSize(QSize(50, 50))
        self.tb_back_home.setAutoRaise(True)
        self.tb_back_home.move(30, 10)
        self.tb_back_home.clicked.connect(self.jump_tb_back_home)

        self.tb_back = QToolButton(self)
        self.tb_back.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back.setIcon(QIcon(image_path+'/tb_back.png'))
        self.tb_back.setIconSize(QSize(50, 50))
        self.tb_back.setAutoRaise(True)
        self.tb_back.move(700, 10)
        self.tb_back.clicked.connect(self.jump_tb_back)
        self.show_information()


    def show_information(self):
        self.tb_QQ = QToolButton(self)
        self.tb_QQ.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_QQ.setText("QQ聊天")  # 设置文字
        self.tb_QQ.setFont(QFont("宋体", 15))
        self.tb_QQ.setIcon(QIcon(image_path+"/tb_QQ.png"))  # 设置图标
        self.tb_QQ.setIconSize(QSize(200, 200))  # 设置图标的大小
        self.tb_QQ.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_QQ.move(150, 100)  # 按钮的位置
        self.tb_QQ.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_QQ.clicked.connect(self.jump_QQ)

        self.tb_weichat = QToolButton(self)
        self.tb_weichat.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb_weichat.setText("微信聊天")  # 设置文字
        self.tb_weichat.setFont(QFont("宋体", 15))
        self.tb_weichat.setIcon(QIcon(image_path+"/tb_weichat.png"))  # 设置图标
        self.tb_weichat.setIconSize(QSize(200, 200))  # 设置图标的大小
        self.tb_weichat.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_weichat.move(400, 100)  # 按钮的位置
        self.tb_weichat.setAutoRaise(True)  # 属性是否保持启动自动升起
        self.tb_weichat.clicked.connect(self.jump_weichat)
        self.show()

    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.fction = FunctionWindow()
        self.hide()

    def jump_QQ(self):
        self.a = QQ()
        self.hide()
    def jump_weichat(self):
        self.b = Weichat()
        self.hide()

class QQ(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('QQ')
        self.setGeometry(0, 10, 800, 480)
        navigation_bar = QToolBar()
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(50, 50))
        self.addToolBar(navigation_bar)

        self.tb_back_home = QAction(QIcon(image_path + '/tb_back_home.png'), '返回', self)
        self.tb_back = QAction(QIcon(image_path + '/tb_back.png'), '返回', self)
        navigation_bar.addAction(self.tb_back_home)
        navigation_bar.addAction(self.tb_back)
        self.tb_back_home.triggered.connect(self.jump_tb_back_home)
        self.tb_back.triggered.connect(self.jump_tb_back)
        self.browser = QWebView()
        # self.browser = QWebEngineView()
        self.browser.load(QUrl('https://im.qq.com/'))
        self.setCentralWidget(self.browser)
        self.show()
    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.fction = Show_information()
        self.hide()

class Weichat(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('微信')
        self.setGeometry(0, 10, 800, 480)
        navigation_bar = QToolBar()
        # 设定图标的大小
        navigation_bar.setIconSize(QSize(50, 50))
        self.addToolBar(navigation_bar)

        self.tb_back_home = QAction(QIcon(image_path + '/tb_back_home.png'), '返回', self)
        self.tb_back = QAction(QIcon(image_path + '/tb_back.png'), '返回', self)
        navigation_bar.addAction(self.tb_back_home)
        navigation_bar.addAction(self.tb_back)
        self.tb_back_home.triggered.connect(self.jump_tb_back_home)
        self.tb_back.triggered.connect(self.jump_tb_back)
        self.browser = QWebView()
        # self.browser = QWebEngineView()
        self.browser.load(QUrl('https://wx.qq.com/'))
        self.setCentralWidget(self.browser)
        self.show()
    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.fction = Show_information()
        self.hide()

class Car_information(BaseWindow):
    def __init__(self):
        super(Car_information, self).__init__()
        self.tb_back_home = QToolButton(self)
        self.tb_back_home.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back_home.setIcon(QIcon(image_path+'/tb_back_home.png'))
        self.tb_back_home.setIconSize(QSize(50, 50))
        self.tb_back_home.setAutoRaise(True)
        self.tb_back_home.move(30, 10)
        self.tb_back_home.clicked.connect(self.jump_tb_back_home)

        self.tb_back = QToolButton(self)
        self.tb_back.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb_back.setIcon(QIcon(image_path+'/tb_back.png'))
        self.tb_back.setIconSize(QSize(50, 50))
        self.tb_back.setAutoRaise(True)
        self.tb_back.move(700, 10)
        self.tb_back.clicked.connect(self.jump_tb_back)
        self.Show_car_information()

    def Show_car_information(self):
        self.tb_gasoline = QToolButton(self)  # 工具按钮得实例化
        self.tb_gasoline.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tb_gasoline.setText("油量\n15L")  # 设置文字
        self.tb_gasoline.setFont(QFont("宋体", 15))
        self.tb_gasoline.setIcon(QIcon(image_path + "/tb_gasoline.png"))  # 设置图标
        self.tb_gasoline.setIconSize(QSize(100, 100))  # 设置图标的大小
        self.tb_gasoline.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_gasoline.resize(200, 110)
        self.tb_gasoline.move(20, 80)  # 按钮的位置
        self.tb_gasoline.setAutoRaise(True)  # 属性是否保持启动自动升起

        self.tb_speed = QToolButton(self)  # 工具按钮得实例化
        self.tb_speed.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tb_speed.setText("车速\n15km/h")  # 设置文字
        self.tb_speed.setFont(QFont("宋体", 15))
        self.tb_speed.setIcon(QIcon(image_path + "/speed.png"))  # 设置图标
        self.tb_speed.setIconSize(QSize(100, 100))  # 设置图标的大小
        self.tb_speed.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_speed.resize(200, 110)
        self.tb_speed.move(20, 220)  # 按钮的位置
        self.tb_speed.setAutoRaise(True)  # 属性是否保持启动自动升起

        self.tb_temperature = QToolButton(self)  # 工具按钮得实例化
        self.tb_temperature.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tb_temperature.setText("车内温度\n25℃")  # 设置文字
        self.tb_temperature.setFont(QFont("宋体", 15))
        self.tb_temperature.setIcon(QIcon(image_path + "/tb_temperature.png"))  # 设置图标
        self.tb_temperature.setIconSize(QSize(100, 120))  # 设置图标的大小
        self.tb_temperature.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_temperature.resize(200, 110)
        self.tb_temperature.move(20, 360)  # 按钮的位置
        self.tb_temperature.setAutoRaise(True)  # 属性是否保持启动自动升起

        self.tb_security = QToolButton(self)  # 工具按钮得实例化
        self.tb_security.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tb_security.setText("车内情况\n无异常")  # 设置文字
        self.tb_security.setFont(QFont("宋体", 15))
        self.tb_security.setIcon(QIcon(image_path + "/tb_security.png"))  # 设置图标
        self.tb_security.setIconSize(QSize(100, 120))  # 设置图标的大小
        self.tb_security.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_security.resize(200, 110)
        self.tb_security.move(300, 80)  # 按钮的位置
        self.tb_security.setAutoRaise(True)  # 属性是否保持启动自动升起

        self.tb_distance = QToolButton(self)  # 工具按钮得实例化
        self.tb_distance.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tb_distance.setText("公里数\n55km")  # 设置文字
        self.tb_distance.setFont(QFont("宋体", 15))
        self.tb_distance.setIcon(QIcon(image_path + "/tb_distance.png"))  # 设置图标
        self.tb_distance.setIconSize(QSize(100, 120))  # 设置图标的大小
        self.tb_distance.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_distance.resize(200, 110)
        self.tb_distance.move(300, 220)  # 按钮的位置
        self.tb_distance.setAutoRaise(True)  # 属性是否保持启动自动升起

        self.tb_security = QToolButton(self)  # 工具按钮得实例化
        self.tb_security.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.tb_security.setText("车内情况\n无异常")  # 设置文字
        self.tb_security.setFont(QFont("宋体", 15))
        self.tb_security.setIcon(QIcon(image_path + "/tb_security.png"))  # 设置图标
        self.tb_security.setIconSize(QSize(100, 120))  # 设置图标的大小
        self.tb_security.setStyleSheet("color:white;border: 2px solid blue")
        self.tb_security.resize(200, 110)
        self.tb_security.move(580, 80)  # 按钮的位置
        self.tb_security.setAutoRaise(True)  # 属性是否保持启动自动升起

        self.show()
    def jump_tb_back_home(self):
        self.back_home = MainWindow()
        self.hide()

    def jump_tb_back(self):
        self.fction = FunctionWindow()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win= MainWindow()
    sys.exit(app.exec_())
