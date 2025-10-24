def describe_colors(weather):
    clouds = weather.get("clouds", 0)
    humidity = weather.get("humidity", 50)

    if clouds < 20:
        color_names = ["zlatistá", "oranžová", "jemne ružová"]
    elif 20 <= clouds <= 60:
        color_names = ["ružová", "fialová", "oranžovo-červená"]
    elif humidity > 70:
        color_names = ["bledoružová", "pastelovo oranžová"]
    else:
        color_names = ["sivé tóny", "neutrálne farby"]

    css_palette = {
        "zlatistá": "#FFD700",
        "oranžová": "#FFA500",
        "jemne ružová": "#FFC0CB",
        "ružová": "#FF69B4",
        "fialová": "#9370DB",
        "oranžovo-červená": "#FF4500",
        "bledoružová": "#FFB6C1",
        "pastelovo oranžová": "#FFDAB9",
        "sivé tóny": "#B0B0B0",
        "neutrálne farby": "#C0C0C0"
    }

    css_colors = [css_palette.get(c, "#FFFFFF") for c in color_names]

    return {
        "names": color_names,
        "css": css_colors
    }
