from pydub import AudioSegment
from aip import AipSpeech
import rpi_project


def text():
    data = rpi_project.get_data(2)
    range = rpi_project.get_config('html')
    txt = ''
    if data[0] < range['temperature_low'] or data[0] > range['temperature_high'] or data[1] < range['humidity_high'] or \
            data[1] > range['humidity_high']:
        txt += '警告，'
    txt += '温度{}摄氏度， 湿度百分之{}，'.format(data[0], data[1])
    return txt

def wav_save(content,path='broadcast.wav'):
    with open('temp','wb') as f:
        f.write(content)
    AudioSegment.from_mp3('temp').export(path,'wav')

settings = rpi_project.get_config('speech')

APP_ID = settings['token']['APPID'] or '15856841'
API_KEY = settings['token']['API_KEY'] or 'nLEzBX0iuZjvoM4TtbEVB6sU'
SECRET_KEY = settings['token']['SECRET_KEY'] or '09IW6spofMr8npiDVmffqGyOT6a2Z9ni'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

result = client.synthesis(text(), 'zh', 1, settings['optional'])
wav_save(result)
