import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
print("API Key:", WEATHER_API_KEY)

# Mapeo clima → Pokémon
CLIMA_POKEMON = {
    "Thunderstorm": "Pikachu",
    "Drizzle": "Psyduck",
    "Rain": "Squirtle",
    "Snow": "Snorunt",
    "Clear": "Charmander",
    "Clouds": "Eevee",
    "Mist": "Gastly",
    "Fog": "Gastly",
    "Haze": "Gastly",
    "Smoke": "Gastly",
    "Dust": "Sandshrew",
    "Sand": "Sandshrew",
    "Ash": "Sandshrew",
    "Squall": "Gyarados",
    "Tornado": "Gyarados"
}

@app.get("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Faltan lat/lon"}), 400

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        main_weather = data["weather"][0]["main"]  # p.ej., "Rain", "Clear"
        pokemon = CLIMA_POKEMON.get(main_weather, "Eevee")  # Eevee por defecto
        return jsonify({
            "lat": lat,
            "lon": lon,
            "condition": main_weather,
            "pokemon": pokemon
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/health")
def health():
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

