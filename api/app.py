from flask import Flask, jsonify, request
app = Flask(__name__)

@app.get("/api/health")
def health():
    return jsonify({"ok": True})

@app.get("/api/weather")
def weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    return jsonify({
        "lat": lat, "lon": lon,
        "condition": "clear",
        "pokemon": "Charmander"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
