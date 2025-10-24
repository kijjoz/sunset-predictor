fetch("/api/sunset")
  .then(res => res.json())
  .then(data => {
    console.log("Dáta z API:", data);

    if (data.error) {
      document.getElementById("output").innerHTML = "<p>Chyba: " + data.error + "</p>";
      return;
    }

    const gradient = `linear-gradient(to bottom right, ${data.css_colors.join(", ")})`;
    document.body.style.background = gradient;

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
    document.getElementById("output").innerHTML = "<p>Chyba pri načítaní údajov.</p>";
  });
