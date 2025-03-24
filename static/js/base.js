// Dark Mode Toggle Script 
  document.addEventListener("DOMContentLoaded", function () {
      const body = document.body;
      const toggleButton = document.getElementById("dark-mode-toggle");
  
      // Check user preference in localStorage
      const savedTheme = localStorage.getItem("theme") || "light";
      
      if (savedTheme === "dark") {
          body.classList.add("dark-mode");
          toggleButton.textContent = "☀️ Light Mode";
      } else {
          body.classList.add("light-mode");
          toggleButton.textContent = "🌙 Dark Mode";
      }
  
      // Toggle theme on button click
      toggleButton.addEventListener("click", function () {
          if (body.classList.contains("dark-mode")) {
              body.classList.remove("dark-mode");
              body.classList.add("light-mode");
              localStorage.setItem("theme", "light");
              toggleButton.textContent = "🌙 Dark Mode";
          } else {
              body.classList.remove("light-mode");
              body.classList.add("dark-mode");
              localStorage.setItem("theme", "dark");
              toggleButton.textContent = "☀️ Light Mode";
          }
      });
  });
