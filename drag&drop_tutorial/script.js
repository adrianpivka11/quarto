/**
 * Táto premenná bude držať referenciu na element,
 * ktorý práve ťaháme.
 */
let draggedStone = null;






/**
 * Táto funkcia sa spustí vo chvíli,
 * keď používateľ začne ťahať stone.
 * 
//   @param {DragEvent} e - drag event
 */
function handleDragStart(e) {
    /**
     * this = konkrétny element .stone,
     * na ktorom nastal dragstart
     */
    draggedStone = this;
    console.log(draggedStone)

    /**
     * Určuje, že chceme robiť presun.
     * Je to informácia pre browser.
     */
    e.dataTransfer.effectAllowed = "move";

    /**
     * Do dataTransfer uložíme id ťahaného elementu.
     * Neskôr pri drop vieme podľa id nájsť správny stone.
     */
    e.dataTransfer.setData("text/plain", this.id);
}


/**
 * Spustí sa po skončení drag operácie.
 * Upraceme si referenciu.
 * 
 * @param {DragEvent} e
 */
function handleDragEnd(e) {
    draggedStone = null;
}













/**
 * Táto funkcia sa spustí opakovane,
 * keď je ťahaný element nad containerom.
 * 
 * Bez preventDefault() drop väčšinou nebude fungovať.
 * 
 * @param {DragEvent} e
 */
function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
}





/**
 * Spustí sa, keď dragged element vstúpi nad container.
 * Použijeme to na vizuálny efekt.
 * 
 * @param {DragEvent} e
 */
function handleDragEnter(e) {
    this.classList.add("dragover");
}





/**
 * Spustí sa, keď dragged element opustí container.
 * Odstránime vizuálny efekt.
 * 
 * @param {DragEvent} e
 */
function handleDragLeave(e) {
    this.classList.remove("dragover");
}





/**
 * Spustí sa, keď pustíme stone nad containerom.
 * Tu sa vykoná skutočný presun DOM elementu.
 * 
 * @param {DragEvent} e
 */
function handleDrop(e) {
    e.preventDefault();

    /**
     * Odstránime zvýraznenie containera.
     */
    this.classList.remove("dragover");

    /**
     * Získame id elementu, ktorý bol uložený pri dragstart.
     */
    const stoneId = e.dataTransfer.getData("text/plain");

    /**
     * Podľa id nájdeme konkrétny DOM element.
     */
    const stoneElement = document.getElementById(stoneId);

    /**
     * appendChild() spraví skutočný presun DOM node.
     * 
     * Ak stone už niekde v DOM existuje, browser ho:
     * 1. odoberie zo starého rodiča
     * 2. vloží do nového rodiča
     * 
     * Toto NIE JE kópia.
     * Toto je reálny presun.
     */
    this.appendChild(stoneElement);
}



/**
 * Keď sa načíta HTML dokument,
 * nastavíme event listenery.
 */
document.addEventListener("DOMContentLoaded", function () {
    /**
     * Nájdeme všetky stone elementy.
     */
    const stones = document.querySelectorAll(".stone");
    

    /**
     * Nájdeme container.
     */
    const container = document.getElementById("target-container");
 
    /**
     * Každému stone nastavíme drag eventy.
     */
    stones.forEach(function (stone) {
        stone.addEventListener("dragstart", handleDragStart);
        stone.addEventListener("dragend", handleDragEnd);
    });

    /**
     * Containeru nastavíme drop eventy.
     */
    container.addEventListener("dragover", handleDragOver);
    container.addEventListener("dragenter", handleDragEnter);
    container.addEventListener("dragleave", handleDragLeave);
    container.addEventListener("drop", handleDrop);
});