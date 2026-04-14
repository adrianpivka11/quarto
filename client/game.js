const quartoURL = "http://127.0.0.1:8000/games";
const statusBox = document.getElementById("status-box");
const boardEl = document.getElementById("board");
const gameIdLabel = document.getElementById("game-id-label");
const containerStonesEl = document.getElementById("container-stones")

const playerField = document.getElementById('stoneforplayer')
const computerField = document.getElementById('stoneforcomputer')

function getGameIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}


function renderBoard(data) {
    boardEl.innerHTML = ""
    let stringForBoard = ``
    const boardJSON = data.state.board 

    for (let keyField of Object.keys(boardJSON)) {
        stringForBoard += `<div class="cell" id="${keyField}"></div>`
    }

    boardEl.innerHTML = stringForBoard

    for (const [key, value] of Object.entries(data.state.board)) {
    
        if (value === null) {continue}
        
        let stone = value
        let cellOnBoard = key
        const stoneElement = buildStoneElementforBoard(stone)
        document.getElementById(cellOnBoard).appendChild(stoneElement)
  
    }}

function renderStones(data) {
    containerStonesEl.innerHTML = "";
    const stonesJSON = data.state.free_stones;
    let stringForStones = ``;

    for (let stone of stonesJSON) {
        stringForStones += buildStoneHTMLstring(stone);
    }

    containerStonesEl.innerHTML = stringForStones;
}


function buildStoneHTMLstring(stone) {
    let klass = `stone`;

    if (stone[0] === "0") klass += ` black`;
    else klass += ` white`;

    if (stone[1] === "0") klass += ` large`;
    else klass += ` small`;

    if (stone[2] === "0") klass += ` round`;
    else klass += ` square`;

    if (stone[3] === "0") klass += ` plus`;
    else klass += ` minus`;

    return `<div class="${klass}" id="${stone}" draggable="true"></div>`;
}


function buildStoneElementforBoard(stone) {
    let klass = `stone`;

    if (stone[0] === "0") klass += ` black`;
    else klass += ` white`;

    if (stone[1] === "0") klass += ` large`;
    else klass += ` small`;

    if (stone[2] === "0") klass += ` round`;
    else klass += ` square`;

    if (stone[3] === "0") klass += ` plus`;
    else klass += ` minus`;

    const stoneElement = document.createElement("div");
    stoneElement.className = klass;
    stoneElement.id = stone;

    return stoneElement
}

function renderStoneForPlayer(data) {
    playerField.innerHTML = "";

    const stoneObject = data.state.stone_for_player;
    console.log(`Rendered stone for player is ${stoneObject}`)
    if (!stoneObject) return;
    const stone = stoneObject.chosen_stone
    console.log(`Ale stone je ${stone}`)
    playerField.innerHTML = buildStoneHTMLstring(stone);
}


function renderGame(data) {
    renderStones(data);
    renderBoard(data);
    renderStoneForPlayer(data);
}


function resetDropZones() {
    const boardCells = document.querySelectorAll("#board .cell");

    computerField.replaceWith(computerField.cloneNode(true));
    playerField.replaceWith(playerField.cloneNode(true));

    const newComputerField = document.getElementById("stoneforcomputer");
    const newPlayerField = document.getElementById("stoneforplayer");

    boardCells.forEach(cell => {
        cell.replaceWith(cell.cloneNode(true));
    });

    return {
        computerField: newComputerField,
        playerField: newPlayerField,
        boardCells: document.querySelectorAll("#board .cell")
    };
}


function enableGiveStonePhase() {
    const stones = document.querySelectorAll("#container-stones .stone");
    const computerDrop = document.getElementById("stoneforcomputer");

    stones.forEach(stone => {
        stone.draggable = true;
        stone.addEventListener("dragstart", handleDragStart);
        stone.addEventListener("dragend", handleDragEnd);
    });

    computerDrop.addEventListener("dragover", handleDragOver);
    computerDrop.addEventListener("dragenter", handleDragEnter);
    computerDrop.addEventListener("dragleave", handleDragLeave);
    computerDrop.addEventListener("drop", giveStoneToComputer);
}


function enablePlaceStonePhase() {
    const playerStone = document.querySelector("#stoneforplayer .stone");
    const boardCells = document.querySelectorAll("#board .cell");

    if (playerStone) {
        playerStone.draggable = true;
        playerStone.addEventListener("dragstart", handleDragStart);
        playerStone.addEventListener("dragend", handleDragEnd);
    }

    boardCells.forEach(cell => {
        cell.addEventListener("dragover", handleDragOver);
        cell.addEventListener("dragenter", handleDragEnter);
        cell.addEventListener("dragleave", handleDragLeave);
        cell.addEventListener("drop", placeStoneOnBoard);
    });
}







async function loadGame() {
    
    const gameId = getGameIdFromURL();
    console.log("ID z URL:", gameId);

    if (!gameId) {
        statusBox.innerHTML = '<span class="error">A parameter id is missing in URL.</span>';
        return;
    }

    gameIdLabel.textContent = `Game ID: ${gameId}`; 

    try {
        const response = await fetch(`${quartoURL}/${gameId}`);

        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }

        const data = await response.json();
        console.log("Načítané dáta hry:", data)
        renderGame(data)
        setupPhase(data)
        
       } 
    
    

    
    catch (error) {
        console.error("Chyba pri načítaní hry:", error);
        statusBox.innerHTML = `<span class="error">Loading game not successful: ${error.message}</span>`;
        renderBoard({});}
        
    
    
    
    }




async function giveStoneToComputer(e) {
    e.preventDefault();
    this.classList.remove("dragover");

    const stoneId = e.dataTransfer.getData("text/plain");
    const requestMessage = { "chosen_stone": stoneId };

    const gameId = getGameIdFromURL();
    const endpoint = `/give-stone-to-computer`;

    const response = await fetch(`${quartoURL}/${gameId}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestMessage)
    });

    if (!response.ok) {
        throw new Error(`HTTP chyba ${response.status}`);
    }

    const data = await response.json();
    console.log("Načítané dáta hry:", data);
   

    renderGame(data);
    setupPhase(data);
}




async function placeStoneOnBoard(e) {
    e.preventDefault();
    this.classList.remove("dragover");

    const stoneId = e.dataTransfer.getData("text/plain");
    const field = this.id;
    console.log(`Polozeny kamen na cell ${field}`)

    const requestMessage = JSON.stringify({
        stone: stoneId,
        field: Number(field)
    });
    console.log(requestMessage)


    const gameId = getGameIdFromURL();
    const endpoint = `/place-stone`;

    const response = await fetch(`${quartoURL}/${gameId}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: requestMessage
    });

    if (!response.ok) {
        throw new Error(`HTTP chyba ${response.status}`);
    }

    const data = await response.json();
    console.log("Response place-stone:", data);
    

    renderGame(data);
    setupPhase(data);
}




function setupPhase(data) {
    const status = data.state.status;
    const stoneForPlayer = data.state.stone_for_player;

    if (status === 'player wins') {
        statusBox.innerHTML = 'Player has won!';
        return;
    }

    if (status === 'computer wins') {
        statusBox.innerHTML = 'Computer has won!';
        return;
    }

    if (status === 'no winner') {
        statusBox.innerHTML = 'No winner.';
        return;
    }

    if (status !== 'playing') {
        console.error('Unknown game status:', status);
        return;
    }

    if (stoneForPlayer === null) {
        statusBox.innerHTML = `Player is giving a stone to Computer, Computer placing the stone.`;
        enableGiveStonePhase();
    } else {
        statusBox.innerHTML = `Computer is given the stone to Player, Player placing.`;
        enablePlaceStonePhase();
    }
}








// 3. PART -  inicialization of program

loadGame();

















// //                2. part of JS code - Drag & Drop functionality for moving stones to board

// /**
//  * Táto premenná bude držať referenciu na element,
//  * ktorý práve ťaháme.
//  */
let draggedStone = null;
// /**
//  * Táto funkcia sa spustí vo chvíli,
//  * keď používateľ začne ťahať stone.
//  * 
// //  @param {DragEvent} e - drag event
//  */
function handleDragStart(e) {
    /**
     * this = konkrétny element .stone,
     * na ktorom nastal dragstart
     */
    draggedStone = this;
    console.log(draggedStone)

//     /**
//      * Určuje, že chceme robiť presun.
//      * Je to informácia pre browser.
//      */
    e.dataTransfer.effectAllowed = "move";

//     /**
//      * Do dataTransfer uložíme id ťahaného elementu.
//      * Neskôr pri drop vieme podľa id nájsť správny stone.
//      */
    e.dataTransfer.setData("text/plain", this.id);
}

function handleDragEnd(e) {
    draggedStone = null;
}

// /**
//  * Táto funkcia sa spustí opakovane,
//  * keď je ťahaný element nad containerom.
//  * 
//  * Bez preventDefault() drop väčšinou nebude fungovať.
//  * 
//  * @param {DragEvent} e
//  */
function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
}



// /**
//  * Spustí sa, keď dragged element vstúpi nad container.
//  * Použijeme to na vizuálny efekt.
//  * 
//  * @param {DragEvent} e
//  */
function handleDragEnter(e) {
    this.classList.add("dragover");
}



// /**
//  * Spustí sa, keď dragged element opustí container.
//  * Odstránime vizuálny efekt.
//  * 
//  * @param {DragEvent} e
//  */
function handleDragLeave(e) {
    this.classList.remove("dragover");
}




// /**
//  * Spustí sa, keď pustíme stone nad containerom.
//  * Tu sa vykoná skutočný presun DOM elementu.
//  * 
//  * @param {DragEvent} e
//  */
function handleDrop(e) {
    e.preventDefault();

//     /**
//      * Odstránime zvýraznenie containera.
//      */
    this.classList.remove("dragover");

//     /**
//      * Získame id elementu, ktorý bol uložený pri dragstart.
//      */
    const stoneId = e.dataTransfer.getData("text/plain");

//     /**
//      * Podľa id nájdeme konkrétny DOM element.
//      */
    const stoneElement = document.getElementById(stoneId);

//     /**
//      * appendChild() spraví skutočný presun DOM node.
//      * 
//      * Ak stone už niekde v DOM existuje, browser ho:
//      * 1. odoberie zo starého rodiča
//      * 2. vloží do nového rodiča
//      * 
//      * Toto NIE JE kópia.
//      * Toto je reálny presun.
//      */
    this.appendChild(stoneElement);
}
















