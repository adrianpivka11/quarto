const pvcBtn = document.getElementById("startPvC-button");
const pvpBtn = document.getElementById("startPvP-button");

const API_BASE_URL = "https://quarto-api.onrender.com";
const quartoURL = `${API_BASE_URL}/games`;
const quartoURLpvp = `${API_BASE_URL}/gamespvp`;
const testEl = document.getElementById("test-loader");

async function newGamePvC() {
    try {

        console.log("Posielam request na:", quartoURL);
        const res = await fetch(quartoURL, { method: "POST" });
        
        console.log("Response status:", res.status);
        console.log("Response ok:", res.ok);
        
        const data = await res.json();
        console.log("Odpoveď zo servera:", data);

        const gameId = data.game_id;
        console.log("gameId:", gameId);

        // Presmerovanie na novu frontend stranku s query parametrom.
        // Live Server si vie otvorit game.html, lebo je to realny subor v projekte.
        window.location.href = `./game.html?id=${gameId}`;
    } catch (error) {
        console.error("Chyba pri vytváraní hry:", error);
    }
}



async function newGamePvP() {
    try {
        const res = await fetch(quartoURLpvp, { method: "POST" });
        const data = await res.json();

        console.log("Odpoveď zo servera:", data);

        const gameId = data.game_id;
        console.log("gameId:", gameId);

        // Presmerovanie na novu frontend stranku s query parametrom.
        // Live Server si vie otvorit game.html, lebo je to realny subor v projekte.
        window.location.href = `./gamepvp.html?id=${gameId}`;
    } catch (error) {
        console.error("Chyba pri vytváraní hry:", error);
    }
}




pvpBtn.addEventListener("click", newGamePvP);

pvcBtn.addEventListener("click", newGamePvC);
