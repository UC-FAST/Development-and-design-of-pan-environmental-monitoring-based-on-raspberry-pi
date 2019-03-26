import json
import time
import rpi_project

class history_list():
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


def history_write(content, path='history.json'):
    with open(path, 'w')as f:
        f.write(content)


def history_update(size, frequency):
    temp_q = history_list(size)
    hum_q = history_list(size)
    while True:
        data=rpi_project.get_data(2)
        temp_q.append(data[0])
        hum_q.append(data[1])
        data = {'temperature': list(temp_q), 'humidity': list(hum_q)}
        history_write(json.dumps(data))
        time.sleep(frequency / 1000)


size, frequency = (rpi_project.get_config('data_record')['max'], rpi_project.get_config('data_record')['frequency'])
history_update(size, frequency)
