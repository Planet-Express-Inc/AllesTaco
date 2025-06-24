/**
 * Sales Overview for Sellers (verkaufsübersicht.js)
 *
 * Displays a list of completed sales for the logged-in seller.
 *
 * Main Features:
 * - Fetches all sales data for the current user
 * - Dynamically loads product details and buyer names for each order
 * - Displays sales on the webpage including title, buyer name, order ID, price, and quantity
 *
 * HTML Requirements:
 * - A container with the ID `orderHistory` to display the sales
 * - A logged-in user with a stored `user_id` in `sessionStorage`
 *
 * Notes:
 * - Additional API calls are made for each order to retrieve product and user information
 */

import { BASE_URL } from '../config.js';

document.addEventListener("DOMContentLoaded", function() {
    const user_id = sessionStorage.getItem("user_id");
    // Get all sells
    fetch(BASE_URL +`/user/sales/${user_id}`, {
      method: 'GET',
      credentials: 'include'})   
        .then(response => response.json())
        .then(orders => {
            console.log(orders)
            const orderHistory = document.getElementById("orderHistory");
            orderHistory.innerHTML = ""; 

            // Show each sell on the html site
            orders.forEach(async order => {
                const orderDiv = document.createElement("div");
                orderDiv.classList.add("order-item");
                const productCall = await fetch(BASE_URL + "/article/" + order.artikel_id);
                const productArray = await productCall.json();
                const product = productArray[0];

                console.log(product);

                const kauferCall = await fetch(BASE_URL + "/user/info/" + order.kaeufer_id);
                const kauferArray = await kauferCall.json();
                const kaufer = kauferArray[0];
                console.log("kauferCall-ID:", kauferArray); 
                orderDiv.innerHTML = `
                    <h3>Artikel: ${product ? product.titel : order.artikel_id}</h3>
                    <p>Kauf-ID: ${order.kauf_id}</p>
                    <p>Käufer: ${kaufer ? kaufer.benutzername  : kaufer.kaeufer_id}</p>
                    <p>Preis: ${order.kaufpreis.toString().replace('.', ',')} €</p>
                    <p>Anzahl: ${order.anzahl}</p>`
                orderHistory.appendChild(orderDiv);
            });
        })
        .catch(error => console.error("Fehler beim Laden der Bestellungen:", error));
});



