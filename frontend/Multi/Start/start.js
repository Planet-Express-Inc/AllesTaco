/**
 * Login, Registration, and Role Selection (login.js)
 *
 * Manages the login process including cookie prompt, role selection (buyer/seller),
 * login, registration, and navigation to the respective user interfaces.
 *
 * Main Features:
 * - Cookie prompt with accept/decline options and info notice
 * - Dynamically displays popups: cookie notice, role selection, login, and registration
 * - Role selection and storage
 * - Login function with role validation, session storage, and redirection:
 *    - Buyer → `/Multi/Kaeufer/kaeufer.html`
 *    - Seller → `/Multi/Verkaeufer/verkaeufer.html`
 * - Registration with password validation (min. 8 characters) and POST to `/user/register`
 * - Login can also be triggered via Enter key
 *
 * HTML Requirements:
 * - Input fields for username, password, first name, last name, and email
 * - Popup containers with the following classes: `.cookie-popup`, `.roll-popup`, `.login-popup`, `.register-popup`
 * - Input radio buttons with `name="roll-button"` for role selection
 * - Input radio buttons with `name="cookie-choice"` for cookie consent
 * - `#password-error` for optional password error display
 *
 * Notes:
 * - The selected role is sent with the login request and stored in the session
 * - The login response is checked to ensure it returns an array of user data
 */

// Globale Variable zum Speichern der gewählten Rolle
let selectedRoll = "";
import { BASE_URL } from '../config.js';
// Enter klicken für login
document.addEventListener("keydown", function(event) {
if (event.key === "Enter") {
    onLogin();
}
});

//function for displaying the cookie popup
window.toggleCookies = function () {
    const choice = document.querySelector('input[name="cookie-choice"]:checked');
    if (!choice) {
        alert("Bitte wähle aus, ob du die Cookies akzeptieren oder ablehnen möchtest." );
        return;
    }

    if (choice.value === "accept") {
        alert("Cookies akzeptiert!");
        showRoll();
    } else {
        alert("Cookies abgelehnt! Aber Cookies sind doch lecker. Überleg nochmal, ob du sie nicht doch akzeptieren möchtest.");
    }
}

// Roule selection function
window.showRoll = function () {
    document.querySelector('.cookie-popup').style.display = 'none';
    document.querySelector('.roll-popup').style.display = 'block';
    document.querySelector('.login-popup').style.display = 'none';
    document.querySelector('.register-popup').style.display = 'none';

}
// set the selected role and save it in session storage
window.getRoll = function (){
    const rollButton = document.querySelector('input[name="roll-button"]:checked');
    if (!rollButton) {
        alert("Bitte wähle eine Rolle (Käufer oder Verkäufer) aus.");
        return false; // Rolle nicht ausgewählt
    }
    selectedRoll = rollButton.value;
   
    sessionStorage.setItem("roll", selectedRoll); 
    return true; // Rolle erfolgreich gespeichert
}

//login function to display the login popup
window.showLogin = function () {
    if (getRoll()) { // Prüft, ob Rolle ausgewählt wurde
        document.querySelector('.roll-popup').style.display = 'none';
        document.querySelector('.login-popup').style.display = 'block';
        document.querySelector('.register-popup').style.display = 'none';

        // Fügt eine dynamische Überschrift hinzu
        const loginPopup = document.querySelector('.login-popup h2');
        loginPopup.innerHTML = `Einloggen im <br>(${selectedRoll}-konto)`; //.innerHTML um <br> zeilenumbruch
    }
}
//sent login request to the server fia fetch API post request
// and handle the response
window.onLogin = async function () {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(BASE_URL + '/user/login', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                benutzername: username,
                password_encrypt: password,
                rolle: selectedRoll
            })
        });

        const data = await response.json();

        if (response.ok) { //Response von Server abfragen
           // Prüfe, ob Antwort ein Array ist und mindestens ein Element enthält
        if (response.ok && Array.isArray(data) && data.length > 0) {
                // save User-ID and username in sessionStorage

                const userData = data[0]; 
                sessionStorage.setItem("user_id", userData.benutzer_id);
                sessionStorage.setItem("username", userData.benutzername);

                alert("Login erfolgreich! Benutzer-ID: " + userData.benutzer_id);

                
                if(selectedRoll == "Verkäufer"){
                   
                   fetch(BASE_URL + `/user/login`, {
                        method: 'GET',
                        credentials: 'include'
                        })
                        .then(response => {
                            return response.json();
                        })
                        .then(data => {
                            console.log(data);
                        })
                        .catch(error => {
                            console.error('Fehler:', error);
                        });
                         window.location.href = "/Multi/Verkaeufer/verkaeufer.html"; // Zielseite ist die verkäufer site
                }else{
                    window.location.href = "/Multi/Kaeufer/kaeufer.html"; // Zielseite ist die käufer site
                }
            } else {
                alert("Login fehlgeschlagen: Benutzer nicht gefunden oder Passwort falsch.");
                console.log("Server-Antwort:", data);
            }
        } else {
            alert("Fehler beim Login: " + response.statusText);
        }
    } catch (error) {
        alert("Netzwerkfehler: " + error.message);
    }
}
//Funktion zum Anzeigen des Registrieren-Popups
window.showRegister = function () {
    document.querySelector('.login-popup').style.display = 'none';
    document.querySelector('.register-popup').style.display = 'block';
}
window.onRegister = async function (){
// Password check
const password = document.getElementById("register-password").value;
const errorDisplay = document.getElementById("password-error");

// At least 8 figures
if (password.length < 8) {
alert("Passwort muss mindestens 8 Zeichen lang sein. \nBitte registrieren Sie sich erneut."); 
return;
}
    const username = document.getElementById('register-username').value;
    const firstname = document.getElementById('register-firstname').value;
    const lastname = document.getElementById('register-lastname').value;
    const mail = document.getElementById('register-mail').value;
    const data = {
        benutzername: username,
        password_encrypt: password,
        vorname: firstname,
        nachname: lastname,
        email: mail,
        rolle: selectedRoll
    };
    const body = JSON.stringify(data);
    console.log(body); // Logge den JSON-String

    try {
            const response = await fetch(BASE_URL +'/user/register', { // await = auf die Vervollständigung eines Promise wartet,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    vorname: firstname,
                    nachname: lastname,
                    benutzername: username,
                    email: mail,
                    rolle: selectedRoll,
                    password_encrypt: password
                })

            });
            

            if (response.ok) {
                alert("Registrierung erfolgreich!");
                showLogin();
            } else {
                alert("Fehler bei der Registrierung: " + response.statusText);
            }
        } catch (error) {
            alert("Netzwerkfehler: " + error.message);
        }
}
