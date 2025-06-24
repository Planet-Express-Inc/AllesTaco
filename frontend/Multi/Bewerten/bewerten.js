/**
 * Rating Script (bewerten.js)
 *
 * This file provides functions for rating a seller.
 * Includes:
 * - Dynamic display and selection of stars (1–5) with keyboard support and ARIA accessibility.
 * - Retrieval of `seller_id` from the URL.
 * - Form handling and submission of the rating as a POST request to the API.
 * - Display of a modal upon successful submission.
 *
 * Expected HTML structure:
 * - A container with stars (spans with `data-wert` attribute).
 * - A hidden input field with ID `sterne-wert`.
 * - A textarea for comments with ID `description`.
 * - A form with ID `bewerten-form`.
 * - A modal with ID `saveModal` to show after successful rating submission.
 */

import { BASE_URL } from '../config.js';

const params = new URLSearchParams(window.location.search);
const sellerID = params.get('seller_id');

document.addEventListener("DOMContentLoaded", () => {
  const sterneContainer = document.getElementById('sterne-container');
  const sterneInput = document.getElementById('sterne-wert');
  const sterneSpans = sterneContainer.querySelectorAll('span');

  // Make stars focusable & screenreader-friendly
  sterneSpans.forEach(stern => {
    stern.setAttribute('tabindex', '0');
    stern.setAttribute('aria-checked', 'false');

    // Keyboard navigation for screen reader/tab users
    stern.addEventListener('keydown', (e) => {
      if (e.key === " " || e.key === "Enter") {
        stern.click();
      }
      // Links/Rechts zur Auswahl der Sterne per Pfeiltasten
      if (e.key === "ArrowRight" && stern.nextElementSibling) {
        stern.nextElementSibling.focus();
      }
      if (e.key === "ArrowLeft" && stern.previousElementSibling) {
        stern.previousElementSibling.focus();
      }
    });

    // Click/Enter sets aria-checked correctly
    stern.addEventListener('click', () => {
      const wert = parseInt(stern.getAttribute('data-wert'));
      sterneInput.value = wert;
      sterneSpans.forEach((s, i) => {
        const sWert = parseInt(s.getAttribute('data-wert'));
        s.classList.toggle('filled', sWert <= wert);
        // ARIA-checked NUR beim ausgewählten Stern
        s.setAttribute('aria-checked', sWert === wert ? 'true' : 'false');
      });
    });
  });
});

document.getElementById('bewerten-form').addEventListener('submit', function (event) {
  event.preventDefault(); 
  // Get all Elements for the Post
  const description = document.getElementById('description').value.trim();
  const sterne = parseInt(document.getElementById('sterne-wert').value, 10);
  const user_id = sessionStorage.getItem("user_id");
  const roll = sessionStorage.getItem("roll");

  const productData = {
    bewerter_id: user_id,
    bewerteter_id: sellerID,
    kommentar: description,
    rolle_des_bewerteten: roll,
    sterne: sterne
  };
  // Send review to server    
  fetch(BASE_URL + "/user/reviews", {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(productData)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Gespeichert:', data);
    document.getElementById('saveModal').style.display = 'flex';
  })
  .catch(error => {
    console.error('Fehler beim Senden:', error);
  });
});
