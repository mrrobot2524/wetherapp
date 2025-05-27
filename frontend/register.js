document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("regEmail").value.trim();
  const password = document.getElementById("regPassword").value;

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const err = await res.json();
      alert("Ошибка: " + (err.detail || "Не удалось зарегистрироваться"));
      return;
    }

    alert("Регистрация успешна! Войдите в систему.");
    window.location.href = "login.html";
  } catch (err) {
    console.error("Ошибка регистрации:", err);
    alert("Ошибка подключения к серверу");
  }
});
