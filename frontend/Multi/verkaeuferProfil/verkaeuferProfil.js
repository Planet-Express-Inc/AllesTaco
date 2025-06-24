/**
 * Seller Profile and Rating Display (seller.js)
 *
 * Displays a seller’s profile including the ratings they have received.
 *
 * Main Features:
 * - Fetches and displays seller information based on the `user_id` in the URL
 * - Calculates and displays the average star rating
 * - Loads and renders individual reviews with comments, star count, and user details
 *
 * HTML Requirements:
 * - An element with the ID `seller-box` for seller information
 * - A container with the ID `bewertung-list` for displaying individual reviews
 *
 * Notes:
 * - Star ratings are rendered using Unicode characters 
 * - Multiple API calls are made to fetch reviewer and reviewee data
 */

import { BASE_URL } from '../config.js';

const params = new URLSearchParams(window.location.search);
const sellerId = parseInt(params.get('user_id'), 10);

document.addEventListener("DOMContentLoaded", async () => {

    const item = document.getElementById('seller-box');
    try
    {   // Get the seller information
        const sellerRes = await fetch(BASE_URL + `/user/info/${sellerId}`);
        const sellerArray = await sellerRes.json();
        const seller = sellerArray[0]; 
        console.log("Verkäuferdaten:", seller);
        // Get the sellers rating
        const ratingRes = await fetch(BASE_URL + `/user/reviews/${sellerId}`);
        const ratingArray = await ratingRes.json();
        const summe = ratingArray.reduce((acc, ratingArray) => acc + ratingArray.sterne, 0);
        const durchschnitt = summe / ratingArray.length;
        const sternegerundet = Math.round(durchschnitt);

        item.innerHTML = `
                <p class="seller">Name: ${seller.benutzername}</p>
                <p class="seller-rating">${renderSterne(sternegerundet)}</p>
            `;
        } catch (error) {
        console.error("Fehler beim Laden:", error);
        }
        loadBewertungen()
});
// Load the reviews
window.loadBewertungen = async function () {
    try {
        
        const response = await fetch(BASE_URL + `/user/reviews/${sellerId}`);
        const data = await response.json();
        const list = document.getElementById('bewertung-list');

        data.forEach(async bewertung => {
            const item = document.createElement('div');
            item.className = 'bewertung';

            const kauferCall = await fetch(BASE_URL + "/user/info/" + bewertung.bewerter_id);
            const kauferArray = await kauferCall.json();
            const kaufer = kauferArray[0];

            const verkauferCall = await fetch(BASE_URL + "/user/info/" + bewertung.bewerteter_id);
            const verkauferArray = await verkauferCall.json();
            const verkaufer = verkauferArray[0];

            item.innerHTML = `
                <p class="bewertung-user">Bewerter: ${kaufer.benutzername}</p>
                <p class="bewertung-user">Bewerteter: ${verkaufer.benutzername}</p>
                <p class="bewertung-sterne">${renderSterne(bewertung.sterne)}</p>
                <p class="bewertung-kommentar">Kommentar: ${bewertung.kommentar}</p>
            `;

            list.appendChild(item);
        });

    } catch (err) {
        console.error('Fehler beim Laden der Bewertungen:', err);
    }
}
// Calculate the number of full and empty stars
window.renderSterne = function (anzahl) {
  const maxSterne = 5;
  console.log(anzahl);
  const sterne = anzahl || 0;
  console.log(sterne);
  return '★'.repeat(sterne) + '☆'.repeat(maxSterne - sterne);
}
