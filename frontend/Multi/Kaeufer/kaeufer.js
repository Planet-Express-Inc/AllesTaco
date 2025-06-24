/**
 * Buyer Dashboard
 *
 * This script displays an overview of purchasable products for the buyer.
 *
 * Main Features:
 * - `loadArticles(start, end)` loads a defined number of articles from the server
 * - `loadQuery(query)` loads articles based on a search term
 * - `showOnHtml(productArray)` renders the articles into the HTML document
 * - `forward()` & `back()` enable navigation through pages of 10 articles each
 *
 * Special Notes:
 * - When a search query is active, normal pagination is disabled
 * - Product images are dynamically loaded using the article ID
 * - Clicking on a product redirects to its detail page
 *
 * HTML Requirements:
 * - A container with ID `product-list` for displaying the articles
 * - Optional: Buttons or links that trigger `forward()` and `back()`
 */

import { BASE_URL } from '../config.js';
let startArticel = 0;
let endArticel = 10;
let noMoreArticel = false;

document.addEventListener("DOMContentLoaded", () => {
  // Get search query form URL
  const params = new URLSearchParams(window.location.search);
  const query = params.get("query") || ""; // Leerer String

  if (query == ""){
    // Load Articels when no query is found
    loadArticles(0,10)
  }else{
    // Load articels with search query
    loadQuery(query);
  }
});
// Load articels with search query
window.loadQuery = async function (query){
  // Hide buttons
  const buttonContainer = document.querySelector('.button-container');
  if (buttonContainer) {
    buttonContainer.style.display = 'none';
  }
  const productRes = await fetch(BASE_URL + `/article/search/${encodeURIComponent(query)}`, {
    method:'GET',
    credentials:'include',
  })
  const productArray = await productRes.json();
  console.log(productArray);
  showOnHtml(productArray);
}


// Load Articels when no query is found
window.loadArticles = async function (start, end){
  // Show buttons
  const buttonContainer = document.querySelector('.button-container');
  if (buttonContainer) {
    buttonContainer.style.display = 'flex';
  }

  const data = {
    "number": end,
    "offset": start
  }
  const productRes = await fetch(BASE_URL + `/article/multiple`, {
    method:'POST',
    credentials:'include',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  const productArray = await productRes.json();
  console.log(productArray);
  if (productArray.length%10 != 0){
    noMoreArticel = true;
  }
  showOnHtml(productArray);

}
// Show the array on the html site
window.showOnHtml = async function (productArray){
  const list = document.getElementById('product-list');
  list.innerHTML = ""; // 
  productArray.forEach(product => {
    if (product.bestand > 0)
    {
      const item = document.createElement('div');
        item.className = 'product';
        // Show on html
        item.innerHTML = `
          <img src="${BASE_URL}/article/picture/${product.artikel_id}" alt="${product.titel}">
          <div class="product-info">
            <h3 class="product-title">${product.titel}</h3>
            <p class="product-description">${product.beschreibung}</p>
            <p class="product-price">Preis: ${product.preis.replace('.', ',')} €</p>
          </div>
        `;
        // Eventlistener when pressed on articel
        item.addEventListener('click', () => {
          window.location.href = `/Multi/Product/product.html?id=${product.artikel_id}`;
        });
        list.appendChild(item);
    }
  });
}
// Go 10 articels back
window.back = function (){
  // If there are no more articels
  if (startArticel==0){
    startArticel = 0;
    alert("Sie sind auf Seite 1");
}else{
  startArticel -= 10;
  noMoreArticel = false;
  loadArticles(startArticel,endArticel);
  }
}
// Show the next 10 articels
window.forward = function (){
  // If there are no more articels
  if (noMoreArticel == true){
    alert("Sie sind auf der letzten Seite");
}else{
  startArticel += 10;
  loadArticles(startArticel,endArticel);
  }
}