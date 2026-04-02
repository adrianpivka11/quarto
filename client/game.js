const quartoURL = "http://127.0.0.1:8000/games";
const statusBox = document.getElementById("status-box");
const gameJsonEl = document.getElementById("game-json");
const boardEl = document.getElementById("board");
const gameIdLabel = document.getElementById("game-id-label");

function getGameIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function renderBoard(gameData) {
    boardEl.innerHTML = "";

    // Ak server vracia board ako pole 4x4, vykresli jeho obsah.
    // Ak board zatial nema, zobrazime aspon prazdnu 4x4 dosku.
    const board = Array.isArray(gameData.board)
        ? gameData.board
        : Array.from({ length: 4 }, () => Array(4).fill(null));

    for (const row of board) {
        for (const cell of row) {
            const div = document.createElement("div");
            div.className = "cell";
            div.textContent = cell ? JSON.stringify(cell) : "prázdne pole";
            boardEl.appendChild(div);
        }
    }
}

async function loadGame() {
    const gameId = getGameIdFromURL();
    console.log("ID z URL:", gameId);

    if (!gameId) {
        statusBox.innerHTML = '<span class="error">V URL chýba parameter id.</span>';
        gameJsonEl.textContent = "Bez game id neviem načítať dáta.";
        return;
    }

    gameIdLabel.textContent = `Game ID: ${gameId}`;

    try {
        const response = await fetch(`${quartoURL}/${gameId}`);

        if (!response.ok) {
            throw new Error(`HTTP chyba ${response.status}`);
        }

        const data = await response.json();
        console.log("Načítané dáta hry:", data);

        statusBox.textContent = "Dáta hry boli úspešne načítané.";
        gameJsonEl.textContent = JSON.stringify(data, null, 2);
        renderBoard(data);
    } catch (error) {
        console.error("Chyba pri načítaní hry:", error);
        statusBox.innerHTML = `<span class="error">Nepodarilo sa načítať hru: ${error.message}</span>`;
        gameJsonEl.textContent = error.stack || String(error);
        renderBoard({});
    }
}

loadGame();
