/**
 * User Menu and Navigation (all.js)
 *
 * This script manages the navigation of the header and footer based on the user role.
 *
 * Main Features:
 * - Displays dynamic menu content based on the stored user role (`roll`)
 * - Shows user information from session storage (`username`, `role`)
 * - Navigates to profile or shopping cart via buttons
 * - Logs out the user and ends the session
 * - Manages dropdown menus for additional functions
 * - Search functionality triggered by the Enter key
 *
 * HTML Requirements:
 * - Elements with IDs: `profil-link`, `warenkorb`, `logoff`, `user-info`, `user-role`, `dropdown-menu`, `search-input`
 * - Sections with `data-role-content="<role>"` for role-based menu display
 * - Search redirects to the buyer page, even for sellers (switching role to 'buyer')
 *
 * Note:
 * - The role is stored in `sessionStorage` and can be set by clicks (via `data-role`)
 * - Multiple DOMContentLoaded listeners are redundant and could be consolidated
 */

import { BASE_URL } from './config.js';

document.addEventListener("DOMContentLoaded", () => {    
  showRoleBasedMenu();
  userData();

  // Profil aufrufen
  const profilLink = document.getElementById("profil-link");
  if (profilLink) {
    profilLink.addEventListener("click", (e) => {
      e.preventDefault();

      const userId = sessionStorage.getItem("user_id");

      if (userId) {
        window.location.href = `/Multi/verkaeuferProfil/verkaeuferProfil.html?user_id=${encodeURIComponent(userId)}`;
      } else {
        alert("Keine Benutzer-ID gefunden.");
      }
    });
  }

  // open shopping cart
  const warenkorb = document.getElementById("warenkorb");
  if (warenkorb) {
    warenkorb.addEventListener("click", (e) => {
      e.preventDefault();
      const userId = sessionStorage.getItem("user_id");
      if (userId) {
        window.location.href = `/Multi/Warenkorb/warenkorb.html?user_id=${encodeURIComponent(userId)}`;
      } else {
        alert("Keine Benutzer-ID gefunden.");
      }
    });
  }


// Logoff User
const logoff = document.getElementById("logoff");
if (logoff) {
  logoff.addEventListener("click", (e) => {
    e.preventDefault();
    sessionStorage.clear();
    fetch(BASE_URL + `/user/logoff`)
      .then(response => response.json())
      .then(data => {
        console.log("Logout-Antwort:", data);
        console.log(data);
        window.location.href = "/index.html";
      });
  });
}

  document.body.addEventListener("click", (e) => {
    const link = e.target.closest('[data-role]');
    if (!link) return;
    e.preventDefault();

    const role = link.getAttribute('data-role');
    const href = link.getAttribute('href');

    sessionStorage.setItem('roll', role);
    window.location.href = href;
  });
});

// Get user data from session storage
function userData() {
  const username = sessionStorage.getItem('username');
  const role = sessionStorage.getItem('roll');
  const userId = sessionStorage.getItem('user_id');

  const userInfoElement = document.getElementById('user-info');
  const userRoleElement = document.getElementById('user-role');

  // Set the dynamic elements
  if (username && userInfoElement) {
    userInfoElement.textContent = 'Angemeldet als: ' + username;
  }

  if (role && userRoleElement) {
    userRoleElement.textContent = `(${role})`;
  }
}

// Create dropdown menu
function showRoleBasedMenu() {
  const role = sessionStorage.getItem('roll');

  const allRoleSections = document.querySelectorAll('[data-role-content]');
  // hide everything
  allRoleSections.forEach(section => {
    section.style.display = 'none'; 
  });
  // Only show the specific role 
  if (role) {
    const visibleSection = document.querySelector(`[data-role-content="${role}"]`);
    if (visibleSection) {
      visibleSection.style.display = 'block'; 
    }
  }
}

// Show dropdown menu
window.toggleDropdown = function() {
  document.getElementById("dropdown-menu").classList.toggle("show");
}

// Click outside the dropdown menu
window.addEventListener("click", function(event) {
  if (!event.target.closest('.dropdown')) {
    document.getElementById("dropdown-menu").classList.remove("show");
  }
});
// Search starts with enter
document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("search-input");
  if (input) {
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        window.suche();
      }
    });
  }
});

// open search
window.suche = function () {
  const input = document.getElementById("search-input");
  const query = input ? input.value.trim() : "";
  const roll = sessionStorage.getItem('roll'); 
  console.log("Hallo hiersuche");

  // Open start site of käufer
  if (roll == 'Käufer') {
    window.location.href = `/Multi/Kaeufer/kaeufer.html?query=${encodeURIComponent(query)}`;
  }
  // Open start site of verkäufer 
  if (roll == 'Verkäufer') {
    sessionStorage.setItem('roll', 'Käufer');
    window.location.href = `/Multi/Kaeufer/kaeufer.html?query=${encodeURIComponent(query)}`;
  }
}
// Search works when clicked on enter
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("search-input");

  if (input) {
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault(); 
        suche(); 
      }
    });
  }
});

// The logo brings you back to the startsite
window.startsite = function () {
  const role = sessionStorage.getItem("roll");
  if (role =="Verkäufer"){
    window.location.href = `/Multi/Verkaeufer/verkaeufer.html`;
  } if (role =="Käufer") {
    window.location.href = `/Multi/Kaeufer/kaeufer.html`;
  } 

}