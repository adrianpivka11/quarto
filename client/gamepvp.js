
const API_BASE_URL = "https://quarto-api.onrender.com";

const quartoURL = `${API_BASE_URL}/gamespvp`;
const statusBox = document.getElementById("status-box");
const boardEl = document.getElementById("board");
const gameIdLabel = document.getElementById("game-id-label");
const containerStonesEl = document.getElementById("container-stones")


let player1DropZone = document.getElementById('player1dropzone')
let player2DropZone = document.getElementById('player2dropzone')

function getGameIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}


function renderBoard(data) {
    // Args: fetched data
    // based on fetch data render board with empty cells each with unique id
    // if board data contains stones, build stone by buildStoneElementforBoard() and append it as child element to the cell that belongs
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
    // just render stones:) by using buildStoneHTMLstring()
    containerStonesEl.innerHTML = "";
    const stonesJSON = data.state.free_stones;
    let stringForStones = ``;

    for (let stone of stonesJSON) {
        stringForStones += buildStoneHTMLstring(stone);
    }

    containerStonesEl.innerHTML = stringForStones;
}


function buildStoneHTMLstring(stone) {
    // Args: stone e.g. "1101"
    // build stones based on id of stone e.g. "1101". by adding css classes
    // Returns:  string `<div class="stone white small round minus" id="1101"></div>`
    let klass = `stone`;

    if (stone[0] === "0") klass += ` black`;
    else klass += ` white`;

    if (stone[1] === "0") klass += ` large`;
    else klass += ` small`;

    if (stone[2] === "0") klass += ` round`;
    else klass += ` square`;

    if (stone[3] === "0") klass += ` plus`;
    else klass += ` minus`;

    return `<div class="${klass}" id="${stone}"></div>`;
}


function buildStoneElementforBoard(stone) {
    // if stone is already placed, this function is used
    // Args: stone e.g. "1101"
    // Returns:  HTMLDivElement <div class="stone white small round minus" id="1101"></div>
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



function renderGame(data) {
    renderStones(data);
    renderBoard(data);
}




function enablePhaseOne() {
    // removes addEventListeners by resetDropZones() to prevent duplicit addEventListeners in following rounds of game
    // add drag & drop functionality to Stones and player1DropZone
    // dropping stone calls back function placeStone(e, messageJSON)
    // messageJSON is information about who is currently placing and giving
    console.log('PHASE ONE JUST BEGUN')
    const { boardCells } = resetDropZones();
    const messageJSON = {"player1_action": "placed_stone",
                         "player2_action": "gave_stone"}
    const stones = document.querySelectorAll("#container-stones .stone");

    stones.forEach(stone => {
        stone.draggable = true;
        stone.addEventListener("dragstart", handleDragStart);
        stone.addEventListener("dragend", handleDragEnd);
    });

    player1DropZone.addEventListener("dragover", handleDragOver);
    player1DropZone.addEventListener("dragenter", handleDragEnter);
    player1DropZone.addEventListener("dragleave", handleDragLeave);
    player1DropZone.addEventListener("drop", (e) => placeStone(e, messageJSON), { once: true });
                                        // ked prebehne drop tak treba vypnut presun ostatnych kamenov a drop do player1Drop. a urobit append child
                                        // potom zapnut cells a vybrany stone draggable 
                                        // add event listener na cell. kde nastane drop, tak na zaklade toho vykonat funkciu ktora 
                                        // odosle request, a na zaklade response vyrenderuje board, status, free_stones
}


function enablePhaseTwo() {
    // same function as enablePhaseOne()
    // differences: player2DropZone, messageJSON
    console.log('PHASE TWO JUST BEGUN')
    const { boardCells } = resetDropZones();
    const stones = document.querySelectorAll("#container-stones .stone");
    const messageJSON = {"player1_action": "gave_stone",
                         "player2_action": "placed_stone"}
     stones.forEach(stone => {
        stone.draggable = true;
        stone.addEventListener("dragstart", handleDragStart);
        stone.addEventListener("dragend", handleDragEnd);
    });

    player2DropZone.addEventListener("dragover", handleDragOver);
    player2DropZone.addEventListener("dragenter", handleDragEnter);
    player2DropZone.addEventListener("dragleave", handleDragLeave);
    player2DropZone.addEventListener("drop", (e) => placeStone(e, messageJSON), { once: true });
}




function placeStone(e, messageJSON){
    // Args: @param {DragEvent} e - drag event, messageJSON
    // finds out to witch dropZone is stone placed
    // the stone is removed from free stones appended to the dropZone .appendChild()
    // removes drag & drop functionality from free stones
    // add drag & drop functionality to the stone
    // add drag & drop functionality to cells on the board which does not have childElemet = stone
    // drop of the stones calls back function place(e, messageJSON)
    e.preventDefault();

    const dropZone = e.currentTarget;
    dropZone.classList.remove("dragover");
    
    const stoneId = e.dataTransfer.getData("text/plain");
    const stoneEl = document.getElementById(stoneId);
    dropZone.appendChild(stoneEl);

    console.log(`Kamen bol prelozeny do ${dropZone}`)

    const stones = document.querySelectorAll("#container-stones .stone");
    stones.forEach(stone => {
        stone.draggable = false;})
    
    const droppedStone = dropZone.querySelector(".stone");
    const boardCells = document.querySelectorAll("#board .cell");

    
    if (droppedStone) {
        droppedStone.draggable = true;
        droppedStone.addEventListener("dragstart", handleDragStart);
        droppedStone.addEventListener("dragend", handleDragEnd);
    }

    boardCells.forEach(cell => {
        if(!cell.firstElementChild){
            cell.addEventListener("dragover", handleDragOver);
            cell.addEventListener("dragenter", handleDragEnter);
            cell.addEventListener("dragleave", handleDragLeave);
            cell.addEventListener("drop", (e) => place(e, messageJSON), { once: true });
        }
    });

}


async function place(e, messageJSON){
    // place the stone - cell.appendChild(stoneEl)
    // sends REQUEST to the server
    // based on data renderGame() and setUpPhase()
    e.preventDefault();

    const cell = e.currentTarget;
    cell.classList.remove("dragover");

    const stoneId = e.dataTransfer.getData("text/plain");
    const field = cell.id;
    const stoneEl = document.getElementById(stoneId);

    console.log(`Polozeny kamen na cell ${field}`);
    cell.appendChild(stoneEl);

    const requestMessage = JSON.stringify({
        stone: stoneId,
        field: Number(field),
        ...messageJSON
    });
    console.log(requestMessage);

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
    // based on fetched data set Phase 1 or Phase 2 if status === "playing"
    // if status is "player1 wins", "player2 wins", "no winner", the game stops and status is being rendered
    const status = data.state.status;
    let player1Action = data.state.player1_action;
    let player2Action = data.state.player2_action;
    const rs = data.state.remaining_stones
    console.log(data.state.player1_action)
    console.log(data.state.player2_action)
    console.log(status)
    console.log(rs)

    console.log("data =", data);
    console.log("data.state =", data.state);
    console.log("p1 =", data.state.player1_action);
    console.log("p2 =", data.state.player2_action);
    console.log("last_move =", data.state.last_move);



    if (status === "player1 wins") {
        statusBox.innerHTML = "Player 1 has won!";
        return;
    }

    if (status === "player2 wins") {
        statusBox.innerHTML = "Player 2 has won!";
        return;
    }

    if (status === "no winner") {
        statusBox.innerHTML = "No winner.";
        return;
    }

    if (status !== "playing") {
        console.error("Unknown game status:", status);
        return;
    }

    if (player1Action === null && player2Action === null) {
        statusBox.innerHTML = `Player 2 is giving a stone to Player 1, Player 1 placing the stone.`;
        console.log("Fáza 1");
        enablePhaseOne();
        return;
    }

    if (player1Action === "placed_stone") {
        statusBox.innerHTML = "Player 1 is giving a stone to Player 2, Player 2 placing the stone.";
        enablePhaseTwo();
        return;
    }

    statusBox.innerHTML = "Player 2 is giving a stone to Player 1, Player 1 placing the stone.";
    enablePhaseOne();
}




async function loadGame() {
    // main function that runs all Front-end
    // getGameIdFromURL() and based on game id makes request on server to get data for renderGame(data) and setupPhase(data)
    
    const gameId = getGameIdFromURL();
    console.log("ID z URL:", gameId);

    if (!gameId) {
        statusBox.innerHTML = '<span class="error">V URL chýba parameter id.</span>';
        return;
    }

    gameIdLabel.textContent = `Game ID: ${gameId}`; 

    try {
        const response = await fetch(`${quartoURL}/${gameId}`);

        if (!response.ok) {
            throw new Error(`HTTP chyba ${response.status}`);
        }

        const data = await response.json();
        console.log("Načítané dáta hry:", data)
        renderGame(data)
        setupPhase(data)
        
       } 
    
    

    
    catch (error) {
        console.error("Chyba pri načítaní hry:", error);
        statusBox.innerHTML = `<span class="error">Nepodarilo sa načítať hru: ${error.message}</span>`;
        renderBoard({});}
        
    
    
    
    }






function resetDropZones() {
    // clears old addEventListeners from Elements
    // Returns:  clear DOM Elements
    // function prevents duplicates of addEventListeners during cycles of game
    const boardCells = document.querySelectorAll("#board .cell");

    player1DropZone.replaceWith(player1DropZone.cloneNode(true));
    player2DropZone.replaceWith(player2DropZone.cloneNode(true));

    player1DropZone = document.getElementById("player1dropzone");
    player2DropZone = document.getElementById("player2dropzone");

    boardCells.forEach(cell => {
        cell.replaceWith(cell.cloneNode(true));
    });

    return {
        player1DropZone,
        player2DropZone,
        boardCells: document.querySelectorAll("#board .cell")
    };
}








// //                Part of JS code - Drag & Drop functionality for moving stones to board

//  * Táto premenná bude držať referenciu na element,
//  * ktorý práve ťaháme.
let draggedStone = null;





//  * Táto funkcia sa spustí vo chvíli,
//  * keď používateľ začne ťahať stone.
// //  @param {DragEvent} e - drag event
function handleDragStart(e) {
    /**
     * this = konkrétny element .stone,
     * na ktorom nastal dragstart
     */
    draggedStone = this;
    console.log(draggedStone)
//      * Určuje, že chceme robiť presun.
//      * Je to informácia pre browser.
    e.dataTransfer.effectAllowed = "move";
//      * Do dataTransfer uložíme id ťahaného elementu.
//      * Neskôr pri drop vieme podľa id nájsť správny stone.
    e.dataTransfer.setData("text/plain", this.id);
}




function handleDragEnd(e) {
    draggedStone = null;
}
//  * Táto funkcia sa spustí opakovane,
//  * keď je ťahaný element nad containerom.
//  * Bez preventDefault() drop väčšinou nebude fungovať.
//  * @param {DragEvent} e
function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
}




//  * Spustí sa, keď dragged element vstúpi nad container.
//  * Použijeme to na vizuálny efekt. 
//  * @param {DragEvent} e
function handleDragEnter(e) {
    this.classList.add("dragover");
}




//  * Spustí sa, keď dragged element opustí container.
//  * Odstránime vizuálny efekt.
//  * @param {DragEvent} e
function handleDragLeave(e) {
    this.classList.remove("dragover");
}




//  * Spustí sa, keď pustíme stone nad containerom.
//  * Tu sa vykoná skutočný presun DOM elementu.
//  * @param {DragEvent} e
function handleDrop(e) {
    e.preventDefault();
//      * Odstránime zvýraznenie containera.
    this.classList.remove("dragover");
//      * Získame id elementu, ktorý bol uložený pri dragstart.
    const stoneId = e.dataTransfer.getData("text/plain");
//      * Podľa id nájdeme konkrétny DOM element.
    const stoneElement = document.getElementById(stoneId);

//      * appendChild() spraví skutočný presun DOM node.
//      * Ak stone už niekde v DOM existuje, browser ho:
//      * 1. odoberie zo starého rodiča
//      * 2. vloží do nového rodiča
    this.appendChild(stoneElement);
}







// 3. PART -  inicialization of program
loadGame();



