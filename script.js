// ===== LOGIN LOGIC =====
const loginForm = document.querySelector("form[action='']") || document.querySelector("#loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.querySelector(".input-box input[placeholder='Username']").value;
    const password = document.querySelector(".input-box input[placeholder='Password']").value;
    const remember = document.querySelector("input[type='checkbox']")?.checked;

    // Get users from localStorage
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
      alert("Login successful!");
      if (remember) {
        localStorage.setItem("rememberedUser", username);
      } else {
        localStorage.removeItem("rememberedUser");
      }
      // Store current user info
      localStorage.setItem("currentUser", JSON.stringify({
        username: user.username,
        email: user.email,
        loginTime: new Date().toISOString()
      }));
      window.location.href = "dashboard.html"; // redirect after login
    } else {
      alert("Invalid username or password.");
    }
  });

  // Auto-fill remembered user
  window.addEventListener("load", () => {
    const rememberedUser = localStorage.getItem("rememberedUser");
    if (rememberedUser) {
      document.querySelector(".input-box input[placeholder='Username']").value = rememberedUser;
      document.querySelector("input[type='checkbox']").checked = true;
    }
  });
}

// ===== SIGN-UP LOGIC =====
const signupForm = document.getElementById("signupForm");
if (signupForm) {
  signupForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.getElementById("newUsername").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    // Get existing users or initialize empty array
    let users = JSON.parse(localStorage.getItem('users') || '[]');
    
    // Check if username or email already exists
    if (users.some(u => u.username === username)) {
      alert("Username already exists. Please choose another.");
      return;
    }
    if (users.some(u => u.email === email)) {
      alert("Email already registered. Please use another email or reset your password.");
      return;
    }

    // Create new user object
    const newUser = {
      username: username,
      email: email,
      password: password, // In production, this should be hashed
      createdAt: new Date().toISOString()
    };

    // Add to users array and save
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    
    alert("Account created successfully! You can now log in.");
    window.location.href = "index.html";
  });
}
