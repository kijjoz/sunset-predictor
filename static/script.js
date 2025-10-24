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
