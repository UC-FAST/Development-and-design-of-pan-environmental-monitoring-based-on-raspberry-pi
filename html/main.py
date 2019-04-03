'''
前端、接口模块
'''
from flask import Flask,Response
import Adafruit_DHT
import json
import sys
from rpi_project import get_data
app = Flask(__name__)
app.debug=True

@app.route("/")
def hello():
    '''
    主页
    '''
    return app.send_static_file('index.html')

@app.route('/ls')
def yeah():
    '''
    查看使用的python的版本，调试用
    '''
    return '<h1>{}</h1>'.format(sys.version)

@app.route('/api/gettmp')
def temp():
    '''
    api接口
    :return: 温湿度数据，json格式
    '''
    data=get_data(2)
    data = {'temperature':data[0],'humidity':data[1]}
    return Response(json.dumps(data),  mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
