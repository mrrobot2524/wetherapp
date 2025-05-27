document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  const formData = new FormData();
  formData.append("username", email);
  formData.append("password", password);

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/login", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      alert("Неверные данные для входа");
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    window.location.href = "index.html";
  } catch (err) {
    console.error("Ошибка авторизации:", err);
    alert("Ошибка сервера");
  }
});
