import speech_recognition as sr
import jieba
import time
import os
import threading
import sys
import nls  # ALI SDK
import pyttsx3  # python -m pip install pyttsx3==2.71  注意版本问题，过高会报错。。
import pyaudio   #3.7版本wheel安装
import wave
from tqdm import tqdm  # pip install tqdm
from playsound import playsound
import pygame     #pip install pygame
#setup

# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()
p = pyaudio.PyAudio()
#setup
CHUNK = 1024  # 块大小
FORMAT = pyaudio.paInt16  # 每次采集的位数
CHANNELS = 1  # 声道数
RATE = 16000  # 采样率：每秒采集数据的次数
cmd = ""
URL="wss://nls-gateway.cn-
AKID = "LTAI5tGc71aLV5sMmb
AKKEY = "XPimfUwDi08jI2
APPKEY = "m9q
TEXT=''
def listeningfunc():
    with m as source:
        #r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        print(audio)
        print("run here")
        with wave.open("assistreturnvoice.wav", 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio.get_wav_data(
            convert_rate=16000,  # audio samples must be 8kHz or 16 kHz
            convert_width=2  # audio samples should be 16-bit
        ))
            wf.close()



class Test_to_sounds(threading.Thread):
    def __init__(self, threadID, file_name, text):
        threading.Thread.__init__(self)
        self.id = threadID
        self.test_file = file_name
        self.text = text
    def test_on_metainfo(self, message, *args):
        print("on_metainfo message=>{}".format(message))

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))
        try:
            self.f.close()
        except Exception as e:
            print("close file failed since:", e)

    def test_on_data(self, data, *args):
        try:
            self.f.write(data)
        except Exception as e:
            print("write data failed:", e)
    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))
    def run(self):
        threadLock.acquire()
        print("thread tts:{} start..".format(self.id))
        self.f = open(self.test_file, "wb+")
        #api 接口结构
        tts = nls.NlsSpeechSynthesizer(
            url=URL,
            akid=AKID,
            aksecret=AKKEY,
            appkey=APPKEY,
            on_metainfo=self.test_on_metainfo,
            on_data=self.test_on_data,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error,
            on_close=self.test_on_close,
            callback_args=[self.id]
        )
        print("{}: API session start".format(self.id))
        r = tts.start(self.text, voice="xiaobei", aformat="mp3")
        print("{}: API tts done with result:{}".format(self.id, r))
        time.sleep(5)
        threadLock.release()

"""pygame 音乐播放"""
class audioplay(threading.Thread):
    def __init__(self, audio):
        threading.Thread.__init__(self)
        self.audio = audio

    def run(self):
        threadLock.acquire()
        pygame.init()
        pygame.mixer.music.load(self.audio)
        pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)  # 音乐结束事件
        pygame.mixer.music.play()
        done = False
        # -------- 主循环 -----------
        while not done:

            for event in pygame.event.get():  # 迭代每个事件
                if event.type == pygame.QUIT:  # 如果单击了关闭按钮
                    done = True  # 此标题为True，进而while循环会退出
                elif event.type == pygame.constants.USEREVENT:
                    # 当音乐播放完毕后会触发此事件
                    done = True
        threadLock.release()

class Sounds_to_text(threading.Thread):  # 语音识别类
    def __init__(self, threadID, filename):
        threading.Thread.__init__(self)
        self.__id = threadID
        self.__test_file = filename
    def test_on_sentence_begin(self, message, *args):
        print("test_on_sentence_begin:{}".format(message))
    def test_on_sentence_end(self, message, *args):
        global cmd
        print("test_on_sentence_end:{}".format(message))
        dict_1 = eval(message)  ###str convert to dict
        print(dict_1)
        print("test_on_sentence_end:{}".format(dict_1["payload"]))
        if ('result' in dict_1["payload"].keys()):
            print("result received")
            cmd = dict_1["payload"]["result"]
            print("current text is ", cmd)
        else:
            pass
    def test_on_start(self, message, *args):
        print("test_on_start:{}".format(message))
    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))
    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))
    def test_on_result_chg(self, message, *args):
        print("test_on_chg:{}".format(message))
    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))
    def run(self):
        # Get lock to synchronize threads

        with open(self.__test_file, "rb") as f:
            self.__data = f.read()
        print("sounds_to texts thread:{} start..".format(self.__id))
        sr = nls.NlsSpeechTranscriber(
            url=URL,
            akid=AKID,
            aksecret=AKKEY,
            appkey=APPKEY,
            on_sentence_begin=self.test_on_sentence_begin,
            on_sentence_end=self.test_on_sentence_end,
            on_start=self.test_on_start,
            on_result_changed=self.test_on_result_chg,
            on_completed=self.test_on_completed,
            on_error=self.test_on_error,
            on_close=self.test_on_close,
            callback_args=[self.__id]
        )
        print("{}: API sounds to text session start".format(self.__id))
        r = sr.start(aformat="pcm",
                     enable_intermediate_result=False,
                     enable_punctutation_prediction=True,
                     enable_inverse_text_normalization=True)
        self.__slices = zip(*(iter(self.__data),) * 640)
        for i in self.__slices:
            sr.send_audio(bytes(i))
            time.sleep(0.01)
        sr.ctrl(ex={"test": "tttt"})
        time.sleep(1)
        r = sr.stop()
        print("{}: sr stopped:{}".format(self.__id, r))
        time.sleep(5)
        # Free lock to release next thread

def tts(cmdstring):
    thread_tts = Test_to_sounds("thread1", "output.mp3", cmdstring)
    thread_tts.start()
    thread_tts.join()
    time.sleep(1)
    thread_audioplay = audioplay("output.mp3")  # 将源码中command = ' '.join(command).encode('utf-16')变为command = ' '.join(command)即可
    thread_audioplay.start()
    thread_audioplay.join()

    os.remove("output.mp3")


def thread_audioplayfunction(audio_file):
    thread_audioplay = audioplay(audio_file)
    thread_audioplay.start()
    thread_audioplay.join()

#todo
def cmdchoice(cmd):
    global voiceflagexit
    if "起床" in str(cmd) :
        print("主人，起床了")
        thread_audioplayfunction("D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/主人该起床啦.mp3")
    elif "吃饭" in  str(cmd) :
        print("主人，吃饭了")
        thread_audioplayfunction(
            "D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/主人吃饭了.mp3")
    elif "回家" in  str(cmd) :
        print("主人，你要回家了吗，注意路上小心，下雨的话记得带伞，记得去接孩子和你老婆。")
        thread_audioplayfunction(
            "D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/主人你要回家了吗.mp3")
    elif "上班" in str(cmd):
        print("主人，你要上班了吗，注意路上小心，下雨的话记得带伞，今天您又是元气满满的一天呢")
        thread_audioplayfunction(
            "D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/主人你要上班了吗.mp3")
    elif "开心" in str(cmd):
        print("开心")
        thread_audioplayfunction(
        "D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/开心.mp3")
    else:
        pass



nls.enableTrace(False)
threadLock = threading.Lock()
threads = []
if __name__ == '__main__':
    while 1:
        # 提示音播放
        try:
            thread_audioplayfunction(
                "D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/notify.wav")
        except:
            pass
        #监听
        listeningfunc()
        #声音转文字
        thread_stt = Sounds_to_text("thread11", "assistreturnvoice.wav")
        threads.append(thread_stt)
        thread_stt.start()  # get text cmd
        thread_stt.join()
        try:
            os.remove("assistreturnvoice.wav")
        except:
            pass
        print(cmd)
        if cmd == '':
            print("没听清楚")
            thread_audioplayfunction(
                "D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/unclear.mp3")
        #热词hut word唤醒
        else:
            voiceflagexit = 1
            while  voiceflagexit:
                result = jieba.lcut(cmd)
                if  "alex" or "爱丽丝" in result:
                    print("hot word detected,alex!")
                    thread_audioplayfunction("D:/pycharm/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10-master/speech_recognition/voice_from_assist/陈运.mp3") # 将源码中command = ' '.join(command).encode('utf-16')变为command = ' '.join(command)即可
                    #语音服务问答FAQ
                    cmdchoice(cmd)
                    # intial cmd result
                    cmd = ''
                    result = ''
                    voiceflagexit = 0

                else:
                    voiceflagexit = 0
                    print("run here while loop else")



