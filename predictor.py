def evaluate_sunset(weather):
    """
    Vyhodnotí, či bude západ slnka pekný podľa počasia.
    Vracia skóre (0–5) a textový verdikt.
    """
    clouds = weather.get("clouds", 50)
    humidity = weather.get("humidity", 70)
    visibility = weather.get("visibility", 10000)
    desc = weather.get("description", "").lower()

    score = 3  # neutrálne

    # menej oblačnosti → lepší západ
    if clouds < 20:
        score += 2
    elif clouds < 50:
        score += 1
    elif clouds > 80:
        score -= 2

    # vysoká vlhkosť → menej sýte farby
    if humidity > 85:
        score -= 1
    elif humidity < 40:
        score += 1

    # zlá viditeľnosť → slabší efekt
    if visibility < 5000:
        score -= 1

    # popis počasia
    if "rain" in desc or "dážď" in desc:
        score -= 2
    elif "clear" in desc or "jasno" in desc:
        score += 1
    elif "cloud" in desc or "oblačno" in desc:
        score -= 0.5

    # ohraničiť výsledok
    score = max(0, min(5, round(score)))

    # textový verdikt
    if score >= 4:
        verdict = "Pekný západ, odporúčame pozrieť"
    elif score >= 2:
        verdict = "Priemerný západ, možno niečo uvidíš"
    else:
        verdict = "Západ slnka dnes nebude výrazný"

    return score, verdict
