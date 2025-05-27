// Проверка авторизации
const token = localStorage.getItem("token");
if (!token) {
  window.location.href = "/static/login.html";
}

const cityInput = document.getElementById("cityInput");
const suggestions = document.getElementById("suggestions");
const resultDiv = document.getElementById("result");
const historyPanel = document.getElementById("historyPanel");
let selectedCity = "";

const weatherIcons = {
  0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
  45: "🌫️", 48: "🌫️", 51: "🌦️", 61: "🌧️",
  71: "❄️", 80: "🌧️", 95: "⛈️", 96: "⛈️"
};

function getCurrentDateTime() {
  const now = new Date();
  return now.toLocaleString("ru-RU", {
    weekday: "long",
    hour: "2-digit",
    minute: "2-digit",
    day: "numeric",
    month: "long"
  });
}

function setBackgroundByTime() {
  const hour = new Date().getHours();
  if (hour >= 6 && hour < 12) {
    document.body.style.background = "linear-gradient(to right, #FFEFBA, #FFFFFF)";
  } else if (hour >= 12 && hour < 18) {
    document.body.style.background = "linear-gradient(to right, #74ebd5, #acb6e5)";
  } else {
    document.body.style.background = "linear-gradient(to right, #141E30, #243B55)";
  }
}
setBackgroundByTime();

const themeToggle = document.getElementById("themeToggle");
if (themeToggle) {
  themeToggle.addEventListener("change", (e) => {
    document.body.classList.toggle("dark", e.target.checked);
  });
}

if (cityInput) {
  cityInput.addEventListener("input", async () => {
    const query = cityInput.value.trim();
    if (query.length < 2) return (suggestions.innerHTML = "");

    try {
      const res = await fetch(`/api/v1/autocomplete?q=${encodeURIComponent(query)}`);
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Ошибка: ${res.status} — ${text}`);
      }
      const cities = await res.json();

      suggestions.innerHTML = "";
      cities.forEach((city) => {
        const li = document.createElement("li");
        li.textContent = city.name;
        li.addEventListener("click", () => {
          cityInput.value = city.name;
          selectedCity = city.name;
          suggestions.innerHTML = "";
        });
        suggestions.appendChild(li);
      });
    } catch (error) {
      console.error("Ошибка автодополнения:", error);
    }
  });
}

const searchBtn = document.getElementById("searchBtn");
if (searchBtn) {
  searchBtn.addEventListener("click", async () => {
    const city = selectedCity || cityInput.value.trim();
    if (!city) return;

    try {
      const res = await fetch(`/api/v1/weather?city=${encodeURIComponent(city)}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Ошибка: ${res.status} — ${text}`);
      }

      const data = await res.json();
      const tempData = data.forecast?.hourly?.temperature_2m?.slice(0, 5) || [];
      const code = data.forecast?.hourly?.weathercode?.[0] ?? 0;
      const icon = weatherIcons[code] || "🌡️";

      resultDiv.innerHTML = `
        <h3>${icon} ${data.city}</h3>
        <p><strong>Сегодня:</strong> ${getCurrentDateTime()}</p>
        <p><strong>Ближайшие температуры:</strong></p>
        <ul>
          ${tempData.map((t) => `<li>${t}°C</li>`).join("")}
        </ul>
      `;

      await fetch(`/api/v1/history`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ city }),
      });

      localStorage.setItem("lastCity", city);
      renderHistory();
    } catch (error) {
      console.error("Ошибка прогноза:", error);
      resultDiv.innerHTML = `<p style="color: red;">Не удалось загрузить прогноз. Попробуйте позже.</p>`;
    }
  });
}

async function renderHistory() {
  if (!historyPanel) return;
  try {
    const res = await fetch("/api/v1/history", {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Не удалось получить историю");

    const history = await res.json();
    historyPanel.innerHTML = "<h4>История:</h4>";
    historyPanel.style.display = "block";
    historyPanel.style.padding = "10px";
    historyPanel.style.background = "#f4f4f4";
    historyPanel.style.borderRight = "2px solid #ccc";
    historyPanel.style.position = "absolute";
    historyPanel.style.left = "0";
    historyPanel.style.top = "0";
    historyPanel.style.height = "100vh";
    historyPanel.style.overflowY = "auto";
    historyPanel.style.minWidth = "150px";

    history.forEach((city) => {
      const item = document.createElement("div");
      item.className = "history-item";
      item.textContent = city;
      item.style.cursor = "pointer";
      item.style.padding = "6px 10px";
      item.style.borderBottom = "1px solid #ccc";
      item.addEventListener("click", () => {
        cityInput.value = city;
        selectedCity = city;
        searchBtn.click();
      });
      historyPanel.appendChild(item);
    });
  } catch (err) {
    console.error("Ошибка истории:", err);
  }
}

renderHistory();

const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "/static/login.html";
  });
}

const clearBtn = document.getElementById("clearBtn");
if (clearBtn) {
  clearBtn.addEventListener("click", async () => {
    try {
      await fetch("/api/v1/history", {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      localStorage.removeItem("lastCity");
      renderHistory();
      alert("История и последний город очищены");
    } catch (error) {
      console.error("Ошибка при очистке:", error);
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const savedCity = localStorage.getItem("lastCity");
  if (savedCity) {
    cityInput.value = savedCity;
    selectedCity = savedCity;
    searchBtn.click();
  }
});
