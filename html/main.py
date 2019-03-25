from flask import Flask,Response
import Adafruit_DHT
import json
import sys
app = Flask(__name__)
app.debug=True

@app.route("/")
def hello():
    return app.send_static_file('index.html')

@app.route('/ls')
def yeah():
    return '<h1>{}</h1>'.format(sys.version)

@app.route('/api/gettmp')
def temp():
    d_hum,d_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,2)
    d_hum = round(d_hum,2)
    d_temp = round(d_temp,2)
    #data = [d_temp,d_hum]
    #return Response(json.dumps(data),  mimetype='application/json')
    data = {'temperature':d_temp,'humidity':d_hum}
    return Response(json.dumps(data),  mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
