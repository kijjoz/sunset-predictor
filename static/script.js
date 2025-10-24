function loadSunsetWithLocation() {
  document.getElementById("output").innerHTML = "<p>Načítavam údaje o západe slnka...</p>";

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        fetch(`/api/sunset?lat=${lat}&lon=${lon}`)
          .then(res => res.json())
          .then(data => {
            if (data.error) {
              document.getElementById("output").innerHTML =
                "<p>Chyba: " + data.error + "</p>";
              return;
            }

            const gradient = `linear-gradient(to bottom right, ${data.css_colors.join(", ")})`;
            document.body.style.background = gradient;

            document.getElementById("output").innerHTML = `
              <h2>${data.verdict}</h2>
              <p><strong>Dátum:</strong> ${data.date}</p>
              <p><strong>Miesto:</strong> ${data.location}</p>
              <p><strong>Čas západu:</strong> ${data.sunset_time}</p>
              <p><strong>Farby oblohy:</strong> ${data.colors.join(", ")}</p>
              <p><strong>Skóre:</strong> ${data.score}</p>
              <p><strong>Počasie:</strong> ${data.weather_data.description}, oblačnosť ${data.weather_data.clouds}%, vlhkosť ${data.weather_data.humidity}%</p>
            `;
          })
          .catch(() => {
            document.getElementById("output").innerHTML =
              "<p>Chyba pri načítaní údajov.</p>";
          });
      },
      (error) => {
        document.getElementById("output").innerHTML =
          "<p>Nepodarilo sa získať polohu. Povoľ GPS v prehliadači.</p>";
      }
    );
  } else {
    document.getElementById("output").innerHTML =
      "<p>Tento prehliadač nepodporuje zistenie polohy.</p>";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("check");
  button.addEventListener("click", loadSunsetWithLocation);
  loadSunsetWithLocation(); // automaticky hneď po načítaní
});
