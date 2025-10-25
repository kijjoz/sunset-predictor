function loadSunset(lat, lon) {
  fetch(`/api/sunset?lat=${lat}&lon=${lon}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("output").innerHTML =
          "<p>Chyba: " + data.error + "</p>";
        return;
      }

      // Nastavenie pozadia
      if (data.css_colors && data.css_colors.length > 0) {
        const gradient = `linear-gradient(to bottom right, ${data.css_colors.join(", ")})`;
        document.body.style.background = gradient;
      }

      // Ak API vrátilo mesto, ale uprednostníme súradnice
      const locationText = data.location.includes(",")
        ? data.location
        : `${data.weather_data.lat.toFixed(2)}, ${data.weather_data.lon.toFixed(2)}`;

      document.getElementById("output").innerHTML = `
        <h2>${data.verdict}</h2>
        <p><strong>Dátum:</strong> ${data.date}</p>
        <p><strong>Miesto:</strong> ${locationText}</p>
        <p><strong>Čas západu:</strong> ${data.sunset_time}</p>
        <p><strong>Farby oblohy:</strong> ${data.colors.join(", ")}</p>
        <p><strong>Skóre:</strong> ${data.score}</p>
        <p><strong>Počasie:</strong> ${data.weather_data.description}, 
           oblačnosť ${data.weather_data.clouds}%, 
           vlhkosť ${data.weather_data.humidity}%</p>
      `;
    })
    .catch(err => {
      console.error("Chyba API:", err);
      document.getElementById("output").innerHTML =
        "<p>Chyba pri načítaní údajov.</p>";
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("check");

  button.addEventListener("click", () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          loadSunset(lat, lon);
        },
        () => {
          // Fallback na Košice
          loadSunset(48.72, 21.26);
        }
      );
    } else {
      loadSunset(48.72, 21.26);
    }
  });

  // Načíta automaticky po načítaní
  button.click();
});
