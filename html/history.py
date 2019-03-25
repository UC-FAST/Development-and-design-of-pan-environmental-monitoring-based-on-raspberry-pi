import json
import Adafruit_DHT
import time


class history_list:
    def __init__(self, size):
        self.list = list()
        self.length = size

    def append(self, data):
        if len(self.list) == self.length:
            del self.list[0]
        self.list.append(data)

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __delitem__(self, key):
        del self.list[key]

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self.list)

def get_config(path='./static/config.json'):
    with open(path, 'r') as f:
        config = json.load(f)
    return config['data_record']['max'], config['data_record']['frequency']


def history_write(content, path='history.json'):
    with open(path, 'w')as f:
        f.write(content)


def history_update(size, frequency):
    temp_q = history_list(size)
    hum_q = history_list(size)
    time_q = history_list(size)
    while True:
        d_hum, d_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 2)
        d_hum = round(d_hum, 2)
        d_temp = round(d_temp, 2)
        temp_q.append(d_temp)
        hum_q.append(d_hum)
        time_q.append(time.strftime('%H:%M:%S',time.localtime(time.time())))
        data = {'time':list(time_q),'temperature': list(temp_q), 'humidity': list(hum_q)}
        history_write(json.dumps(data))
        time.sleep(frequency / 1000)


size, frequency = get_config()
history_update(size, frequency)
