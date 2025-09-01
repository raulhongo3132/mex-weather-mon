import os
import requests
from flask import Flask, jsonify, request
from math import ceil

app = Flask(__name__)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

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

LAT_START, LAT_END = 14.5, 32.5
LON_START, LON_END = -118, -86
STEP = 4
cached_grid = None
weather_cache = {}

def get_weather(lat, lon):
    key = (lat, lon)
    if key in weather_cache:
        return weather_cache[key]

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    main_weather = r.json()["weather"][0]["main"]
    pokemon = CLIMA_POKEMON.get(main_weather, "Eevee")
    weather_cache[key] = {"lat": lat, "lon": lon, "condition": main_weather, "pokemon": pokemon}
    return weather_cache[key]



@app.get("/api/grid")
def grid():
    global cached_grid
    lat_min = float(request.args.get("lat_min", LAT_START))
    lat_max = float(request.args.get("lat_max", LAT_END))
    lon_min = float(request.args.get("lon_min", LON_START))
    lon_max = float(request.args.get("lon_max", LON_END))

    grid_data = []
    lat = lat_min
    while lat <= lat_max:
        lon = lon_min
        while lon <= lon_max:
            try:
                grid_data.append(get_weather(round(lat,4), round(lon,4)))
            except Exception as e:
                print("Error:", e)
            lon += STEP
        lat += STEP

    return jsonify(grid_data)


# NUEVO ENDPOINT
@app.get("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return jsonify({"error": "Faltan lat/lon"}), 400
    try:
        lat = float(lat)
        lon = float(lon)
        data = get_weather(lat, lon)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- FINAL: levantar servidor ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)


