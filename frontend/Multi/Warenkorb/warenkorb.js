/**
 * Shopping Cart Management and Checkout (warenkorb.js)
 *
 * Displays all items in the current user's shopping cart and enables purchase.
 *
 * Main Features:
 * - Retrieves all items in the current user's shopping cart
 * - Displays item details including dynamic quantity selection
 * - Automatically calculates and updates the total price when quantities change
 * - Deletes individual items from the cart
 * - Processes the purchase, including rebuilding the cart with updated quantities
 * - Shows a confirmation modal after successful checkout
 *
 * HTML Requirements:
 * - Container with ID 'product-card' for displaying products
 * - Element with ID 'total-price' for showing the total amount
 * - Modal with ID 'review-modal' for purchase confirmation
 *
 * Notes:
 * - Prices are formatted accordingly
 * - During checkout, all items are removed and re-added with updated quantities before completing the purchase
 */

import { BASE_URL } from '../config.js';

let productsData = [];

document.addEventListener("DOMContentLoaded", () => {
  const list = document.getElementById('product-card');
  const totalPriceElement = document.getElementById('total-price');

  // Formate the price
  function formatPrice(price) {
    return price.toFixed(2).replace('.', ',') + ' €';
  }
  // Calculate the total price after changing the ammount
  window.updateTotalPrice = function () {
    let total = 0;
    const products = list.querySelectorAll('.product');
    products.forEach(product => {
      const priceText = product.querySelector('.product-price').textContent;
      const priceMatch = priceText.match(/Preis:\s*([\d.,]+)\s*€/);

      if (priceMatch) {
        const price = parseFloat(priceMatch[1].replace(',', '.'));
        total += price;
      }
    });
      totalPriceElement.textContent = formatPrice(total);

  // Activate or deactivate buy button 
  const purchaseButton = document.getElementById('buy-button');
  if (purchaseButton) {
    purchaseButton.disabled = total === 0;
    purchaseButton.classList.toggle('disabled', total === 0);
  }
};
  // Shows all Articels which are in the shoping cart
  async function loadArticles() {
    try {
      const response = await fetch(BASE_URL + `/user/cart`, { method: 'GET', credentials: 'include' });
      const data = await response.json();
      productsData = data;

      for (const articels of data) {
        const productRes = await fetch(BASE_URL + `/article/${articels.artikel_id}`);
        const productArray = await productRes.json();
        const product = productArray[0];

        const item = document.createElement('div');
        item.className = 'product';

        const basePrice = parseFloat(product.preis);

        item.innerHTML = `
          <img src="${BASE_URL}/article/picture/${product.artikel_id}" alt="${product.titel}">
          <div class="product-info">
            <h3 class="product-title">${product.titel}</h3>
            <p class="product-description">${product.beschreibung}</p>
            <p class="product-id">Artikel ID: ${product.artikel_id}</p>
            <p class="product-seller">Verkäufer: ${product.verkaeufer_id}</p>
            <p class="product-price" id="price-${product.artikel_id}">Preis: ${formatPrice(basePrice)}</p>

            <div class="product-actions">
              <label for="quantity-${product.artikel_id}">Menge:</label>
              <select id="quantity-${product.artikel_id}" class="quantity-select">
                  ${[...Array(product.bestand)].map((_, i) => `<option value="${i + 1}">${i + 1}</option>`).join("")}
              </select>

              <button onclick="deleteArticelButton(${product.artikel_id})" class="delete-button">Löschen</button>
            </div>
          </div>
        `;

        const quantitySelect = item.querySelector(`#quantity-${product.artikel_id}`);
        const priceElement = item.querySelector(`#price-${product.artikel_id}`);

        quantitySelect.addEventListener('change', () => {
          const selectedQuantity = parseInt(quantitySelect.value, 10);
          const totalPrice = basePrice * selectedQuantity;
          priceElement.textContent = `Preis: ${formatPrice(totalPrice)}`;
          updateTotalPrice();
        });

        list.appendChild(item);
      }

      updateTotalPrice();
    } catch (err) {
      console.error('Fehler beim Laden der Produkte:', err);
    }
  }

  loadArticles();
});

// The action when the deleted button was pressed
window.deleteArticelButton = async function (id) {
  await deleteArticel(id);
  window.location.href = "/Multi/Warenkorb/warenkorb.html";
  console.log("das ist ein ausgabe");
}

// Removes an articel from the shoping cart
window.deleteArticel = async function (id) {
  try {
    const response = await fetch(BASE_URL + `/user/cart/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    });

    if (response.status === 204) {
      console.log('Erfolgreich gelöscht (204)');
    } else {
      console.error('Fehler beim Löschen: HTTP-Status', response.status);
      alert("Löschen fehlgeschlagen. Fehlercode: " + response.status);
    }
  } catch (error) {
    console.error('Fehler beim Senden:', error);
    alert("Ein technischer Fehler ist aufgetreten.");
  }
};



// Buy the shoping cart and shows a success window
window.buy = async function () {
  const list = document.getElementById('product-card');
  const products = list.querySelectorAll('.product');

  const artikelInfos = await getElements(products);
  console.log("Ausgabe ", artikelInfos);
  // Delete the current shoping cart
  for (const artikel of artikelInfos) {
  await deleteArticel(artikel.artikel_id);
  console.log("Artikel ID:", artikel.artikel_id);
  }
  // Add all articels in the shoping cart with new ammount
  for (const artikel of artikelInfos) {
  await addArticel(artikel);
  console.log("Hier ist ein langer Text damit ich das besser sehe:", artikel);
  }
  // Buy the new shoping cart
  try {
    await fetch(BASE_URL + `/user/purchase`, {
    method: 'POST',
    credentials: 'include'
  });

  const modal = document.getElementById("review-modal");
  modal.style.display = "block";
  } catch (error) {
    console.error('Fehler beim Kauf:', error);
  }
};

// Add new Articel to shoping cart
window.addArticel = async function (article) {
  try {
    console.log("Test ", article);
    const response = await fetch(BASE_URL + `/user/cart`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(article)
    });
    const data = await response.json();
    console.log('Hinzugefügt:', data);    
  } catch (error) {
    console.error('Fehler beim Senden:', error);
  }
}

// Get the values of the html site
window.getElements = async function (products){
  const userId = sessionStorage.getItem("user_id");
  const artikelInfos = [];

  try {
    for (const product of products) {
    const artikelId = parseInt(product.querySelector('.product-id').textContent.match(/Artikel ID:\s*(\d+)/)[1],10);
    const quantitySelect = product.querySelector('.quantity-select');
    const anzahl = parseInt(quantitySelect.value, 10);

    const productRes = await fetch(BASE_URL + `/article/${artikelId}`);
    const productArray = await productRes.json();
    const produkt = productArray[0];

    artikelInfos.push({
      artikel_id: artikelId,
      benutzer_id: userId,
      verkaeufer_id: produkt.verkaeufer_id,
      anzahl: anzahl
    });
      }
      console.log(artikelInfos);
      await new Promise(resolve => setTimeout(resolve, 1000));
      return artikelInfos;
      
  } catch (error) {
    console.error('Fehler beim Kauf:', error);
  }
  
}
// Go to Startseite 
window.startseite = function () {
  window.location.href = "/Multi/Kaeufer/kaeufer.html";
};
// Go to Bestellhistorie
window.bestellhistorie = function () {
  window.location.href = "/Multi/orderHistory/orderHistory.html";
};
