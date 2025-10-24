function loadSunset(city, dayOffset) {
  fetch(`/api/sunset?city=${city}&day=${dayOffset}`)
    .then(res => res.json())
    .then(data => {
      console.log("Dáta z API:", data);

      if (data.error) {
        document.getElementById("output").innerHTML =
          "<p>Chyba: " + data.error + "</p>";
        return;
      }

      // Nastavenie pozadia podľa predpokladaných farieb oblohy
      if (data.css_colors && data.css_colors.length > 0) {
        const gradient = `linear-gradient(to bottom right, ${data.css_colors.join(", ")})`;

        // Plynulá animácia prechodu medzi farbami
        document.body.animate(
          [
            { background: document.body.style.background },
            { background: gradient }
          ],
          {
            duration: 1500,
            fill: "forwards",
            easing: "ease-in-out"
          }
        );

        // Nastav novú farbu po dokončení animácie
        document.body.style.background = gradient;
      }

      // Výpis údajov do HTML
      document.getElementById("output").innerHTML = `
        <h2>${data.verdict}</h2>
        <p><strong>Dátum:</strong> ${data.date}</p>
        <p><strong>Mesto:</strong> ${data.location}</p>
        <p><strong>Čas západu:</strong> ${data.sunset_time}</p>
        <p><strong>Farby oblohy:</strong> ${data.colors.join(", ")}</p>
        <p><strong>Skóre:</strong> ${data.score}</p>
        <p><strong>Počasie:</strong> ${data.weather_data.description}, oblačnosť ${data.weather_data.clouds}%, vlhkosť ${data.weather_data.humidity}%</p>
      `;
    })
    .catch((err) => {
      console.error("Chyba API:", err);
      document.getElementById("output").innerHTML =
        "<p>Chyba pri načítaní údajov.</p>";
    });
}

// Po načítaní stránky
document.addEventListener("DOMContentLoaded", () => {
  const citySelect = document.getElementById("city");
  const daySelect = document.getElementById("day");
  const button = document.getElementById("check");

  // Po kliknutí na tlačidlo načítaj nové údaje
  button.addEventListener("click", () => {
    const city = citySelect.value;
    const dayOffset = daySelect.value;
    loadSunset(city, dayOffset);
  });

  // Automatické načítanie pre Košice dnes
  loadSunset("Kosice", 0);
});
