'''
历史记录模块
'''
import json
import time
import rpi_project

path = 'history.json'  # 历史记录文件路径


class history_list():
    '''
    历史记录类，FIFO
    '''

    def __init__(self, length: int):
        '''
        历史记录列表初始化
        :param length: 最大长度
        '''
        self.list = list()
        self.length = length

    def append(self, data):
        '''
        增加历史记录，超出限定个数删除第一个数据
        :param data: 历史数据
        :return: None
        '''
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


def history_write(data: dict, path: str = path):
    '''
    将记录写入文件
    :param data: 历史记录，dict格式
    :param path: 历史记录文件路径，
    :return: None
    '''
    with open(path, 'w')as f:
        f.write(json.dumps(data))


def history_load(path: str = path):
    '''
    载入先前的历史记录
    :param path: 历史记录文件路径
    :return: 如果文件存在且合法，返回文件数据（dict格式），否则返回None
    '''
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError or FileNotFoundError:
            return None


def history_update(length: int, frequency: int):
    '''
    更新历史记录文件
    :param length: 记录保存长度
    :param frequency: 采样间隔，毫秒
    :return: None
    '''
    temp_q = history_list(length)
    hum_q = history_list(length)
    time_q = history_list(length)
    history_data = history_load()
    if history_data:
        temp_q = history_data['temperature'][:length]
        time_q = history_data['time'][:length]
        hum_q = history_data['humidity'][:length]
    while True:
        data = rpi_project.get_data(2)
        temp_q.append(data[0])
        hum_q.append(data[1])
        time_q.append(time.strftime("%H:%M:%S", time.localtime()))
        data = {'temperature': list(temp_q), 'humidity': list(hum_q), 'time': list(time_q)}
        history_write(data)
        time.sleep(frequency / 1000)


if __name__ == '__main__':
    length, frequency = (
        rpi_project.get_config('data_record')['max'],
        rpi_project.get_config('data_record')['frequency']
    )
    history_update(length, frequency)
