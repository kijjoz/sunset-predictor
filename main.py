from datetime import datetime
from flask import Flask, render_template, jsonify
from predictor import evaluate_sunset
from sunset_calc import get_sunset_time
from color_description import describe_colors
from weather_service import get_weather

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/sunset")
def get_sunset_prediction():
    weather_data = get_weather()
    if not weather_data:
        return jsonify({"error": "Nepodarilo sa získať údaje o počasí"}), 500

    sunset_time = get_sunset_time("Kosice")
    score, verdict = evaluate_sunset(weather_data)
    colors = describe_colors(weather_data)
    today = datetime.now().strftime("%d.%m.%Y")

    print("Predikované farby:", colors)

    return jsonify({
        "location": "Košice",
        "date": today,
        "sunset_time": sunset_time.strftime("%H:%M"),
        "verdict": verdict,
        "colors": colors["names"],
        "css_colors": colors["css"],
        "score": score,
        "weather_data": weather_data
    })

if __name__ == "__main__":
    app.run(debug=True)
