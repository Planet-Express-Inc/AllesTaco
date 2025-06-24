/**
 * Product Creation (newProduct.js)
 *
 * Allows the seller to add a new product.
 * The central element is a form where all required product information must be provided.
 *
 * Main Features:
 * - Validation of input fields and image selection
 * - Conversion of the uploaded image to Base64 for transmission
 * - Creation of a product object with all attributes (title, description, price, etc.)
 * - Sending product data via POST request to the API (/article)
 * - Image preview after selection
 *
 * HTML Requirements:
 * - Form with ID `product-form`
 * - Input fields with IDs: `title`, `description`, `kategorie`, `price`, `amount`, `image-upload`
 * - Image preview element with ID `preview`
 * - Confirmation popup with ID `saveModal`
 */

import { BASE_URL } from '../config.js';

document.getElementById('product-form').addEventListener('submit', function (event) {
  event.preventDefault(); 
  // Get the value from the form
  const title = document.getElementById('title').value.trim();
  const description = document.getElementById('description').value.trim();
  const kategorie = document.getElementById('kategorie').value.trim();
  const price = parseFloat(document.getElementById('price').value);
  const amount = parseFloat(document.getElementById('amount').value);
  const imageInput = document.getElementById('image-upload');
  const file = imageInput.files[0];

  if (!file) {
    alert("Bitte ein Bild auswählen.");
    return;
  }
  // Build the data for the database
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
    console.log(JSON.stringify(productData, null, 2)); 
    // Push the values to the API/Databbase
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

// Get uploaded Picture
document.getElementById('image-upload').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      const preview = document.getElementById('preview');
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
});