'''
绘图模块
'''

import json
import matplotlib.pyplot as plt

with open('history.json', 'r')as f:
    data = json.load(f)


def data_plot(data: dict = data, out: str = 'history.png', size: tuple = (50, 10)):
    '''
    根据data绘制图像
    :param data: 数据，dict格式
    :param out: 图像保存路径
    :param size: 图像大小，tuple格式
    :return:None
    '''
    fig = plt.figure(figsize=size)

    ax1 = fig.add_subplot(111)
    time = data['time']
    temperature = data['temperature']
    humidity = data['humidity']
    ax1.plot(time, temperature, 'r', label='temperature')
    ax1.set_ylabel('temperature')
    plt.xticks(rotation=30)

    ax2 = plt.twinx(ax1)
    ax2.plot(time, humidity, 'b', label='humidity')
    ax2.set_ylabel('humidity')
    ax2.set_xlabel('time')
    fig.legend(loc=1)
    plt.title('history data')
    plt.grid()
    plt.grid(axis='x')
    plt.savefig(out)


if __name__ == '__main__':
    data_plot(data)
