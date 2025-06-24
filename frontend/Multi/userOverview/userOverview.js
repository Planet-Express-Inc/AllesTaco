/**
 * Display User Profile (profil.js)
 *
 * Displays all user data for the currently logged-in user.
 *
 * Main Features:
 * - Loads user data based on `user_id` from `sessionStorage` (`/user/info/:id`)
 * - Displays first name, last name, email, username, and role in the profile section
 * - Shows different sections depending on the user role:
 *    - For "seller": displays reviews and link to sales (`/verkauferVerkaufe`)
 *    - For other roles: shows link to order history (`/orderHistory`)
 * - Optionally shows submitted reviews for sellers via `/user/reviews/:id`
 * - Star ratings are rendered graphically
 *
 * HTML Requirements:
 * - `userDetails`: container to display user profile data
 * - `userCommentsSection`: optional section for seller reviews (initially hidden)
 * - `order-link-to-role`: navigation link for sales or order history
 * - `userComments`: section for displaying reviews
 */

import { BASE_URL } from '../config.js';

  document.addEventListener("DOMContentLoaded", function () {
    // Benutzerdaten laden
    
    fetch(BASE_URL +"/user/info/" + sessionStorage.getItem("user_id") )
      
      .then(response => response.json())
      .then(users => {
        const user = users[0];
        console.log("Benutzerdaten:", user);
        const details = document.getElementById("userDetails");
        details.innerHTML = `
          <div><strong>Vorname:</strong> ${user.vorname}</div>
          <div><strong>Nachname:</strong> ${user.nachname}</div>
          <div><strong>Mail:</strong> ${user.email}</div>
          <div><strong>Benutzername:</strong> ${user.benutzername}</div>
          <div><strong>Rolle:</strong> ${sessionStorage.getItem("roll")}</div>
          
        `;
  
        // if rolle is "Verkäufer", show user comments section and link to sales
        if (sessionStorage.getItem("roll") === "Verkäufer") {
          document.getElementById("userCommentsSection").style.display = "block";
          document.getElementById("order-link-to-role").href = "/Multi/verkauferVerkaufe/verkauferVerkaufe.html";
          document.getElementById("order-link-to-role").textContent = "Verkäufe";
          document.getElementById("order-link-to-role").style.display = "block";
          
          loadBewertungen();


        }else{
          document.getElementById("order-link-to-role").href = "/Multi/orderHistory/orderHistory.html";
          document.getElementById("order-link-to-role").textContent = "Bestellungen";
          document.getElementById("order-link-to-role").style.display = "block";
        }

      })
      .catch(error => console.error("Fehler beim Laden der Benutzerdaten:", error));
  });


  
window.loadBewertungen = async function () {
    try {
        // APi Call to fetch user reviews
        const response = await fetch(BASE_URL + `/user/reviews/${sessionStorage.getItem("user_id")}`);
        const data = await response.json();

        const list = document.getElementById('userComments');



        // render the reviews in the userComments section
        data.forEach(bewertung => {
            const item = document.createElement('div');
            item.className = 'bewertung';
            
            item.innerHTML = `
                <p class="bewertung-user">Bewerter: ${bewertung.bewerter_id}</p>
                <p class="bewertung-user">Bewerteter: ${bewertung.bewerteter_id}</p>
                <p class="bewertung-sterne">${renderSterne(bewertung.sterne)}</p>
                <p class="bewertung-kommentar">Kommentar: ${bewertung.kommentar}</p>
            `;

            list.appendChild(item);
        });

    } catch (err) {
        console.error('Fehler beim Laden der Bewertungen:', err);
    }
}


window.renderSterne = function (anzahl) {
  const maxSterne = 5;
  console.log(anzahl);
  const sterne = anzahl || 0;
  console.log(sterne);
  return '★'.repeat(sterne) + '☆'.repeat(maxSterne - sterne);
}