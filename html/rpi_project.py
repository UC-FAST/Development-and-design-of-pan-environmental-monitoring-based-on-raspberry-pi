import json
import Adafruit_DHT

def get_config(item, path='static/config.json'):
    with open(path, 'r') as fp:
        return json.load(fp)[item]

def get_data(pin,number=2):
    d_hum, d_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
    d_hum = round(d_hum, number)
    d_temp = round(d_temp, number)
    return d_temp,d_hum
