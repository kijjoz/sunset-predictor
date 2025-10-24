from flask import Flask, render_template, jsonify, request
from datetime import datetime
from predictor import evaluate_sunset
from sunset_calc import get_sunset_time
from color_description import describe_colors
from weather_service import get_weather
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/sunset")
def get_sunset_prediction():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    # Ak chýba poloha, použijeme default (Košice)
    if lat is None or lon is None:
        lat, lon = 48.72, 21.26

    sunset_time = get_sunset_time(lat=lat, lon=lon)
    weather_data = get_weather(lat=lat, lon=lon, sunset_time=sunset_time)
    if not weather_data:
        return jsonify({"error": "Nepodarilo sa získať údaje o počasí"}), 500

    sunset_time = get_sunset_time(lat=lat, lon=lon)
    score, verdict = evaluate_sunset(weather_data)
    colors = describe_colors(weather_data)
    today = datetime.now().strftime("%d.%m.%Y")

    return jsonify({
        "location": f"{round(lat, 2)}, {round(lon, 2)}",
        "date": today,
        "sunset_time": sunset_time.strftime("%H:%M"),
        "verdict": verdict,
        "colors": colors["names"],
        "css_colors": colors["css"],
        "score": score,
        "weather_data": weather_data
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
