from time import sleep
import history
import rpi_project
import mail
import plot
import speech


def broadcast():
    pass


def emergency_mail():
    '''
    温湿度邮件警告
    '''
    print('dadida')
    while True:
        if rpi_project.data_emergency(2):
            print('mailing')
            data = rpi_project.get_data(2)
            mail.send("温度{}，湿度{}".format(data[0], data[1]))
            sleep(rpi_project.get_config('smtp')['cool_down'])
        else:
            sleep(5)


def emergency_smoke():
    '''
    烟雾邮件警告
    '''
    while True:
        if rpi_project.smoke_detected(18):
            data = rpi_project.get_data(2)
            mail.send("探测到烟雾，温度{}，湿度{}".format(data[0], data[1]))
            sleep(rpi_project.get_config('smtp')['cool_down'])
        else:
            sleep(5)


def historiographer():
    '''
    历史记录
    '''
    size, frequency = (rpi_project.get_config('data_record')['max'], rpi_project.get_config('data_record')['frequency'])
    history.history_update(size, frequency)
