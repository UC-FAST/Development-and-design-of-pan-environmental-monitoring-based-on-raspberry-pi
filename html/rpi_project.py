'''
传感器模块
'''
import json
import RPi.GPIO as GPIO
import Adafruit_DHT

def get_config(item:str, path='static/config.json'):
    '''
    解析配置文件
    :param item: 配置文件项目路径
    :param path: 配置文件路径
    :return: 配置数据，dict格式
    '''
    with open(path, 'r') as fp:
        return json.load(fp)[item]


def get_data(pin, number=2):
    '''
    获取dht22传感器温湿度数据
    :param pin: 输入引脚号
    :param number: 四舍五入保留位数
    :return: (温度,湿度),tuple格式
    '''
    while True:
        d_hum, d_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
        if d_hum and d_temp:
            break
    d_hum = round(d_hum, number)
    d_temp = round(d_temp, number)
    return d_temp, d_hum


def data_emergency(pin):
    '''
    根据设定值监测数据是否超标
    :param pin: dht22输入引脚
    :return: 超标返回True，否则返回False
    '''
    config = get_config('html')
    data = get_data(pin)
    return data[0] < config['temperature_low'] or data[0] > config['temperature_high'] or \
           data[1] < config['humidity_low'] or data[1] > config['humidity_low']


def smoke_detected(pin):
    '''
    Mq2烟雾探测模块
    :param pin: 输入引脚号
    :return: 有烟雾返回True，否则返回False
    '''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    #GPIO.cleanup()
    return not GPIO.input(pin)


