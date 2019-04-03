'''
文字语言转换模块
'''
from pydub import AudioSegment
from aip import AipSpeech
import rpi_project


def text():
    '''
    获取温湿度数据，作为播报内容
    :return: 文本消息
    '''
    data = rpi_project.get_data(2)
    range = rpi_project.get_config('html')
    txt = ''
    if data[0] < range['temperature_low'] or data[0] > range['temperature_high'] or data[1] < range['humidity_high'] or \
            data[1] > range['humidity_high']:
        txt += '警告，'
    if rpi_project.smoke_detected(18):
        txt += '探测到烟雾'
    txt += '温度{}摄氏度， 湿度百分之{}，'.format(data[0], data[1])
    return txt


def wav_save(content, path='broadcast.wav'):
    '''
    写入由百度api返回的音频数据
    :param content: 百度api返回数据，mp3格式
    :param path: 音频文件保存路径
    :return: None
    '''
    with open('temp', 'wb') as f:
        f.write(content)
    AudioSegment.from_mp3('temp').export(path, 'wav')

def speech_api():
    '''
    调用百度api获取语音数据
    :return: None
    '''
    settings = rpi_project.get_config('speech')

    APP_ID = settings['token']['APPID'] or '15856841'
    API_KEY = settings['token']['API_KEY'] or 'nLEzBX0iuZjvoM4TtbEVB6sU'
    SECRET_KEY = settings['token']['SECRET_KEY'] or '09IW6spofMr8npiDVmffqGyOT6a2Z9ni'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis(text(), 'zh', 1, settings['optional'])
    wav_save(result)
