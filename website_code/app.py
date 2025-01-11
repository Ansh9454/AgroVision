from flask import Flask, render_template, jsonify
import requests
import time

app = Flask(__name__)

CHANNEL_ID = '2800421'
API_KEY = 'NDCWC397CZJLULAB'
URL = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={API_KEY}&results=1'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    response = requests.get(URL)
    if response.status_code == 200:
        feed = response.json()['feeds'][0]
        data = {
            'temperature': feed['field1'],
            'humidity': feed['field2'],
            'water_level': feed['field3'],
            'npk': feed['field4'],
            'moisture': feed['field5'],
            'timestamp': int(time.mktime(time.strptime(feed['created_at'], "%Y-%m-%dT%H:%M:%SZ")))
        }

        recommendations = []
        if float(data['water_level']) < 20: 
            recommendations.append('Water level is low, please refill the water tank.')
        if float(data['temperature']) > 35: 
            recommendations.append('Temperature is high, consider cooling measures.')
        if float(data['humidity']) < 30:  
            recommendations.append('Humidity is low, consider using a humidifier.')
        if float(data['npk']) < 10:  
            recommendations.append('NPK level is low, please fertilize the soil.')
        if float(data['moisture']) < 10: 
            recommendations.append('Soil moisture is low, consider irrigation.')

        data['recommendations'] = recommendations

    else:
        data = {}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
