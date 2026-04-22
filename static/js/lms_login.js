function togglePassword() {
    const pass = document.getElementById("password");
    pass.type = pass.type === "password" ? "text" : "password";
}

async function login() {
    const btn = document.getElementById("loginBtn");
    const error = document.getElementById("error");

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    error.innerText = "";

    // loader
    btn.innerHTML = "Loading...";
    btn.disabled = true;

    try {
        const res = await fetch("/lms/login", {
            method: "POST",
            body: new URLSearchParams({   // ✅ FIX: form-data send
                email: email,
                password: password
            })
        });

        // ✅ IMPORTANT: backend redirect handle
        if (res.redirected) {
            window.location.href = res.url;   // auto redirect
            return;
        }

        // fallback (rare case)
        const text = await res.text();
        error.innerText = text;

    } catch (err) {
        error.innerText = "Server error";
    }

    btn.innerText = "Login";
    btn.disabled = false;
}