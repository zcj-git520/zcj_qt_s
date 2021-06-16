"""
这是调用百度语音接口的包：
将语音的采集、语音的识别、语音的合成打包为一个文件
方便使用百度语音,提供交互
"""
from pyaudio import PyAudio ,paInt16   #语音录音
import numpy as np
import wave                           #保存为wav格式的音频
from aip import AipSpeech             #调用百度的API
import pygame
import time, sys
import setting
import logging
"""百度语音的id,key,密钥，可直接在百度免费申请"""
APP_ID = setting.APP_ID
API_KEY = setting.API_KEY
SECRET_KEY = setting.SECRET_KEY
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)   #调用百度api,并生成client的对象
sleep_time = setting.sleep_time  #语音播放时间
systeam_voice = setting.systeam_voice
speak_fliename = setting.speak_fliename
class recoder_voice:
    """
    初始化函数，音频的参数
    录音的函数，将声音数据保存在列表中
    音频生成函数，将声音数据生成音频文件
    参数:录音音频文件名（以及保存位置）
    无返回值
        """
    def __init__(self):
        self.NUM_SAMPLES = 2000          #设置pyaudio的内置缓冲区的大小
        self.samplng_data = 16000        #设置采样频率
        self.count_num = 20              #
        self.save_length = 8              #声音记录的最小长度
        self.time_count = 60         #录音时间，s
        self.level = 500                 #保存声音的阀值
        self.voice_buffer = []
    def redecor(self):
        self.pa = PyAudio()
        self.stream = self.pa.open(format=paInt16,channels=1,rate =self.samplng_data,input=True,
                         frames_per_buffer=self.NUM_SAMPLES)
        self.save_count = 0
        save_buffer =[]
        self.time_ = self.time_count
        while True:
            self.time_  -= 1
            #读入数据
            self.string_data = self.stream.read(self.NUM_SAMPLES)
            #将读入的数据抓换为数组
            self.audio_data = np.fromstring(self.string_data,dtype=np.short)
            #计算大于LEVEL的采样的个数
            self.large_sample_count =np.sum(self.audio_data>self.level)
            if self.large_sample_count >self.count_num:
                self.save_count =  self.save_length
            else:
                self.save_count -=1
            if self.save_count < 0:
                self.save_count =0
            if self.save_count >0:
                #将数据保存在save_buff[]
                save_buffer.append(self.string_data)
            else:
                #将save_buffer中的数据写入wav文件，
                if len(save_buffer) >0:
                    self.voice_buffer = save_buffer
                    save_buffer =[]
                    logging.info("录音提前录取完成")
                    return True
            if self.time_ == 0:
                if len(save_buffer) >0:
                    self.voice_buffer = save_buffer
                    save_buffer =[]
                    logging.info("录音成功")
                    return True
                else:
                    return False
    def savewav(self,filename):
        self.wf = wave.open(filename,"wb")
        self.wf.setnchannels(1)
        self.wf.setsampwidth(2)
        self.wf.setframerate(self.samplng_data)
        self.wf.writeframes(np.array(self.voice_buffer).tostring())
        self.wf.close()
def _recognition(filename):
    """
    语音识别函数：
    :参数: 音频文件名（不在同文件夹需将带上音频路径）
    :返回值:无错误的情况下：返回识别的文字，
            有错误的情况下：返回音频错误信息
    """
    try:
        fp = open(filename,"rb")
        voice_data = fp.read()
        recognition_data = client.asr(voice_data,"wav",16000,{'dev_pid':1936,})
        if recognition_data["err_msg"] == "success.":
            print(recognition_data["result"][0])
            return recognition_data["result"][0]
        else:
            return recognition_data["error_msg"]
    except Exception as e:
        logging.warning("语音识别没有成功，可能没有文件或者没有网络")
        return 0
def speak(text,sleep_time = sleep_time):
    """
    text :语音转文字的文本文档
    speak_flienamw :临时语音文档
    :return: 无
    """
    try:
        speak_data = client.synthesis(text, 'zh', 2, {'vol': 6, 'per': 1, 'spd': 4, 'pit': 4})
        pygame.quit()
        fp = open(speak_fliename, "wb")
        fp.write(speak_data)
        fp.close()

        pygame.mixer.init(frequency=16000)
        pygame.mixer.music.load(speak_fliename)
        pygame.mixer.music.play()
        time.sleep(sleep_time)
        pygame.quit()

    except Exception as e:
        logging.warning(e)
def play_systeam(voice_file = systeam_voice):
    pygame.mixer.init(frequency=16000)
    pygame.mixer.music.load(voice_file)
    pygame.mixer.music.play()
    time.sleep(1)
    pygame.quit()