function loadSunset(lat, lon) {
  fetch(`/api/sunset?lat=${lat}&lon=${lon}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        document.getElementById("output").innerHTML =
          "<p>Chyba: " + data.error + "</p>";
        return;
      }

      // Nastavenie pozadia podľa farieb
      if (data.css_colors && data.css_colors.length > 0) {
        const gradient = `linear-gradient(to bottom right, ${data.css_colors.join(", ")})`;
        document.body.style.background = gradient;
      }

      // Výpis údajov
      document.getElementById("output").innerHTML = `
        <h2>${data.verdict}</h2>
        <p><strong>Dátum:</strong> ${data.date}</p>
        <p><strong>Miesto:</strong> ${data.location}</p>
        <p><strong>Čas západu:</strong> ${data.sunset_time}</p>
        <p><strong>Farby oblohy:</strong> ${data.colors.join(", ")}</p>
        <p><strong>Skóre:</strong> ${data.score}</p>
        <p><strong>Počasie:</strong> ${data.weather_data.description}, 
           oblačnosť ${data.weather_data.clouds}%, 
           vlhkosť ${data.weather_data.humidity}%</p>
      `;
    })
    .catch((err) => {
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
        (pos) => {
          const lat = pos.coords.latitude.toFixed(2);
          const lon = pos.coords.longitude.toFixed(2);
          loadSunset(lat, lon);
        },
        () => {
          // fallback: Košice
          loadSunset(48.72, 21.26);
        }
      );
    } else {
      loadSunset(48.72, 21.26);
    }
  });

  // automaticky načíta po otvorení
  button.click();
});
