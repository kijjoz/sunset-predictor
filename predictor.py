def evaluate_sunset(weather):
    clouds = weather["clouds"]
    humidity = weather["humidity"]
    visibility = weather["visibility"]
    desc = weather["weather"].lower()

    score = 0
    if clouds < 20:
        score += 2
    elif 20 <= clouds <= 60:
        score += 3
    if humidity < 70:
        score += 1
    if visibility > 8000:
        score += 2
    if "rain" in desc or "storm" in desc:
        score -= 3

    if score >= 6:
        verdict = "Veľmi pekný západ slnka"
    elif score >= 4:
        verdict = "Pekný západ, odporúčame pozrieť"
    elif score >= 2:
        verdict = "Priemerný západ"
    else:
        verdict = "Západ slnka pravdepodobne nebude viditeľný"

    return score, verdict
