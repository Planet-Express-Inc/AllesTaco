/**
 * Product Editing Script (editProduct.js)
 *
 * Enables sellers to edit existing products.
 *
 * Main Features:
 * - Loads product information based on the article ID from the URL.
 * - Populates the form with existing product data.
 * - Allows uploading a new image with live preview.
 * - Completely deletes the old product via a DELETE request.
 * - Re-creates the product with updated information via a POST request.
 * - Displays a confirmation modal upon successful editing.
 *
 * Expected HTML Elements:
 * - Form with ID `product-form`
 * - Input fields for title, description, category, price, stock
 * - File upload field with ID `image-upload`
 * - Image preview with ID `preview`
 * - Modal with ID `saveModal`
 *
 * Requirements:
 * - Article ID must be passed as a `articelid` query parameter
 * - A new image must be selected (mandatory)
 */

import { BASE_URL } from '../config.js';
let articelId = 0;

document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(window.location.search);
  articelId = parseInt(params.get('articelid'), 10);
  if (isNaN(articelId)) return;

  try {
    const productRes = await fetch(BASE_URL + `/article/${articelId}`);
    const productArray = await productRes.json();
    const product = productArray[0];  

    // show the attributes of the seleted product
    document.getElementById('product-title').value = product.titel;
    document.getElementById('product-description').textContent = product.beschreibung;
    document.getElementById('product-kategorie').value = product.kategorie;
    document.getElementById('product-price').value = product.preis;
    document.getElementById('product-amount').value = product.bestand;
    document.getElementById('preview').src = BASE_URL + `/article/picture/${product.artikel_id}`
  } catch (error) {
    console.error("Fehler beim Laden:", error);
  }
});

// Upload the new values
document.getElementById('product-form').addEventListener('submit', function (event) {
  event.preventDefault(); 
  const title = document.getElementById('product-title').value.trim();
  const description = document.getElementById('product-description').value.trim();
  const kategorie = document.getElementById('product-kategorie').value.trim();
  const price = parseFloat(document.getElementById('product-price').value);
  const amount = parseFloat(document.getElementById('product-amount').value);
  const imageInput = document.getElementById('image-upload');
  const file = imageInput.files[0];

  if (!file) {
    alert("Bitte ein neues Bild auswählen.");
    return;
  }

  const reader = new FileReader();
  reader.onload = function () {
    const base64Image = reader.result
    const userId = parseInt(sessionStorage.getItem('user_id'), 10);

    const productData = {
      titel: title, 
      verkaeufer_id: userId, 
      beschreibung: description, 
      preis: price, 
      bild: base64Image,  
      status: "verfügbar", 
      bestand: amount, 
      kategorie: kategorie 

    };

    // Removes the old product   
    fetch(BASE_URL + `/article/${articelId}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Fehler beim Löschen');
      }
      return response.text();
    })
    .then(data => {
      console.log('Erfolgreich gelöscht:', data);
    })
    .catch(error => {
      console.error('Fehler:', error);
    });

    // Adds the new product
    fetch(BASE_URL + `/article`, {
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
  };

  reader.readAsDataURL(file); 
});

// Picture preview
document.getElementById('image-upload').addEventListener('change', function (event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();

  reader.onload = function (e) {
    const base64Image = e.target.result; 
    document.getElementById('preview').src = base64Image;
  };

  reader.readAsDataURL(file);
});

