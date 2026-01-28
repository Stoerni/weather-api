from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 API Key aus Environment Variable
API_KEY = os.environ.get("OPENWEATHER_KEY")
if not API_KEY:
    raise ValueError("OPENWEATHER_KEY ist nicht gesetzt!")

# Root Route für Info
@app.route("/")
def index():
    return "Weather API is running. Use /weather?city=CityName"

# Wetter-Endpoint
@app.route("/weather")
def weather():
    city = request.args.get("city", "Barcelona")
    # Sicherheitsfilter: nur Buchstaben, Leerzeichen, Bindestriche
    city = "".join(c for c in city if c.isalpha() or c in " -")
    if len(city) > 50:
        return jsonify({"error": "Ungültige Stadt"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=de"
    
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return jsonify(r.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Port 10000 von Render empfohlen
    app.run(host="0.0.0.0", port=10000)
