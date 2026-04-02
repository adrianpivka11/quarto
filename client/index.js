const pvcBtn = document.getElementById("startPvC-button");
const pvpBtn = document.getElementById("startPvP-button");
const quartoURL = "http://127.0.0.1:8000/games";
const testEl = document.getElementById("test-loader");

async function newGamePvC() {
    try {
        const res = await fetch(quartoURL, { method: "POST" });
        const data = await res.json();

        console.log("Odpoveď zo servera:", data);

        const gameId = data.game_id;
        console.log("gameId:", gameId);

        testEl.innerHTML = gameId;

        // Presmerovanie na novu frontend stranku s query parametrom.
        // Live Server si vie otvorit game.html, lebo je to realny subor v projekte.
        window.location.href = `./game.html?id=${gameId}`;
    } catch (error) {
        console.error("Chyba pri vytváraní hry:", error);
    }
}

pvpBtn.addEventListener("click", () => {
    testEl.innerHTML = "00000000";
    console.log("YES");
});

pvcBtn.addEventListener("click", newGamePvC);
