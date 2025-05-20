from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def format_unix_time(unix_time, timezone_offset=0):
    try:
        return datetime.utcfromtimestamp(unix_time + timezone_offset).strftime('%H:%M:%S')
    except:
        return ""

def get_weather_details(city, country="india"):
    API_KEY = "7ee1f244e7445e55474283055857afaf"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or 'main' not in data:
            return None

        timezone_offset = data.get("timezone", 0)

        weather = {
            "temperature": f"{data['main']['temp']} °C",
            "feels_like": f"{data['main']['feels_like']} °C",
            "description": data['weather'][0]['description'].title(),
            "humidity": f"{data['main']['humidity']}%",
            "wind": f"{data['wind']['speed']} m/s",
            "pressure": f"{data['main']['pressure']} hPa",
            "visibility": f"{data.get('visibility', 0)/1000:.1f} km",
            "sunrise": format_unix_time(data['sys']['sunrise'], timezone_offset),
            "sunset": format_unix_time(data['sys']['sunset'], timezone_offset),
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            "updated": format_unix_time(data['dt'], timezone_offset),
        }

        return weather

    except Exception as e:
        print("Error:", e)
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    location = ""
    country = "india"

    if request.method == 'POST':
        location = request.form.get('location', '')
        country = request.form.get('country', 'india').lower().strip()
        weather = get_weather_details(location, country)

        if not weather:
            weather = {"error": "Could not fetch weather data."}

    return render_template('index.html', weather=weather, location=location.title(), country=country.title())

if __name__ == '__main__':
    app.run(debug=True)

