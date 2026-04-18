# Quarto Game

## Overview
Quarto Game is a small full-stack implementation of the board game Quarto.
**Play here:** https://quarto-game.netlify.app/

The project contains:
- a Python backend built with FastAPI,
- a browser frontend written in HTML, CSS, and JavaScript,
- two game modes: Player vs Computer and Player vs Player.

The backend stores active games in memory and exposes REST endpoints for game creation, loading state, giving stones, and placing stones on the board.  
The frontend renders the board and uses drag-and-drop interactions for gameplay.

Game Modes
----------
1. Player vs Computer
- Player chooses a free stone for the computer.
- Computer places that stone randomly on the board.
- If the game continues, the computer gives a random stone to the player.
- Player places that stone on the board.

2. Player vs Player
- One player chooses a stone for the other player.
- The receiving player places it on the board.
- Players alternate between giving and placing stones.

---

## Live Deployment
- **Play here:** https://quarto-game.netlify.app/

- **Frontend:** Netlify
- **Backend API:** Render

Frontend sends requests to the deployed backend API hosted on Render.

---

## Project Structure

```text
quarto/
├── client/
│   ├── index.html
│   ├── index.js
│   ├── game.html
│   ├── game.js
│   ├── gamepvp.html
│   ├── gamepvp.js
│   ├── index.css
│   ├── games2.css
│   └── ...
├── server/
│   ├── main.py
│   └── requirements.txt
├── drag&drop_tutorial/
├── program_logic.txt
├── quarto_api_architecture.txt
└── README.md


Requirements
------------
Recommended environment:
- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic


## Technologies Used

### Backend
- Python 3
- OOP (Object-Oriented Programming)
- FastAPI
- RESTful API Development
- JSON Serialization / Deserialization
- UUID-based Session Handling
- CORS Middleware

### Frontend
- HTML5
- CSS3
- JavaScript ES6+
- DOM Manipulation
- Drag and Drop API
- Fetch API
- Async / Await
- Responsive Design

### Tools
- Git
- GitHub
- Postman
- Visual Studio Code
- Live Server

### Software Engineering Concepts
- Client–Server Architecture
- Game State Management
- Turn-based System Design
- Frontend–Backend Integration
- Event-driven Programming


Known Limitations
-----------------
- No persistent storage or database.
- No automated tests yet.
- Backend logic is concentrated in one file (`main.py`), which is workable for a
  small study project but would usually be split into multiple modules in a larger app.
- PvP game flow depends on action markers (`player1_action`, `player2_action`) sent
  from the frontend.
- Not playable on mobile devices

