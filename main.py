from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
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
    city = request.args.get("city", "Kosice")
    day_offset = int(request.args.get("day", 0))

    weather_data = get_weather(city)
    if not weather_data:
        return jsonify({"error": "Nepodarilo sa získať údaje o počasí"}), 500

    target_date = datetime.now() + timedelta(days=day_offset)
    sunset_time = get_sunset_time(city, target_date)
    score, verdict = evaluate_sunset(weather_data)
    colors = describe_colors(weather_data)
    today = target_date.strftime("%d.%m.%Y")

    return jsonify({
        "location": city,
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
