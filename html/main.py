'''
前端、接口模块
'''
from flask import Flask,Response,render_template
import json
import sys
from rpi_project import get_data,smoke_detected
from camera_pi import Camera
app = Flask(__name__)
app.debug=True

@app.route('/camera')
def index():
    """Video streaming home page."""
    return render_template('index.html')
 
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/")
def hello():
    '''
    主页
    '''
    return app.send_static_file('index.html')

@app.route('/control')
def control():
    return app.send_static_file('control.html')

@app.route('/ls')
def yeah():
    '''
    查看使用的python的版本，调试用
    '''
    return '<h1>{}</h1>'.format(sys.version)

@app.route('/api/forward')
def forward():
    print('forward')
    return app.send_static_file('control.html')

@app.route('/api/gettmp')
def temp():
    '''
    api接口
    :return: 温湿度数据，json格式
    '''
    data=get_data(2)
    data = {'temperature':data[0],'humidity':data[1],'smoke':smoke_detected()}
    return Response(json.dumps(data),  mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
