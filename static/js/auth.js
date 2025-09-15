document.addEventListener("DOMContentLoaded", () => {
  // --- LOGIN FORM LOGIC ---
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = loginForm.username.value;
      const password = loginForm.password.value;

      const response = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (response.ok) {
        window.location.href = "/dashboard";
      } else {
        alert(`Login Failed: ${data.message}`);
      }
    });
  }

  // --- REGISTER FORM LOGIC (NEW) ---
  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = registerForm.username.value;
      const password = registerForm.password.value;

      const response = await fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Registration successful! Please log in.");
        window.location.href = "/login-page"; // Redirect to login page
      } else {
        alert(`Registration Failed: ${data.message}`);
      }
    });
  }
});
