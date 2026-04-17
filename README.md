Quarto Game
===========

Overview
--------
Quarto Game is a small full-stack implementation of the board game Quarto.
The project contains:
- a Python backend built with FastAPI,
- a browser frontend written in HTML, CSS, and JavaScript,
- two game modes: Player vs Computer and Player vs Player.

The backend stores active games in memory and exposes REST endpoints for game creation,
loading state, giving stones, and placing stones on the board. The frontend renders the
board and uses drag-and-drop interactions for gameplay.

Project Structure
-----------------
quarto/
- quarto.py                Main backend file with game logic, request models, and API endpoints
- client/
  - index.html             Main menu page
  - index.js               Frontend logic for starting a new game
  - game.html              Player vs Computer game page
  - game.js                Frontend logic for Player vs Computer mode
  - gamepvp.html           Player vs Player game page
  - gamepvp.js             Frontend logic for Player vs Player mode
  - games2.css             Shared gameplay styling
  - index.css              Menu styling
- program_logic.txt        Notes describing the game logic
- quarto_api_architecture.txt  API design notes
- drag&drop_tutorial/      Experimental drag-and-drop learning files

Requirements
------------
Recommended environment:
- Python 3.11+
- FastAPI
- Uvicorn
- Pydantic

Install dependencies for the backend for example with:

    pip install fastapi uvicorn pydantic

How to Run the Project
----------------------
1. Start the backend server from the project root:

    uvicorn quarto:app --reload

2. Open the frontend files through a local static server.
   For example, in VS Code you can use Live Server and open:

    client/index.html

3. Make sure the frontend and backend use compatible local addresses:
- Backend API base URL in JS files: http://127.0.0.1:8000
- Frontend allowed origins in FastAPI CORS:
  - http://127.0.0.1:5500
  - http://localhost:5500

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

API Summary
-----------
Player vs Computer:
- POST /games
- GET /games/{game_id}
- POST /games/{game_id}/give-stone-to-computer
- POST /games/{game_id}/place-stone

Player vs Player:
- POST /gamespvp
- GET /gamespvp/{game_id}
- POST /gamespvp/{game_id}/place-stone

Implementation Notes
--------------------
- Games are stored only in memory in the global `games` dictionary.
  Restarting the backend clears all active games.
- The computer move currently uses random selection for both choosing a field
  and choosing the next stone for the player.
- The frontend relies on drag-and-drop and re-renders the full game state after
  each backend response.

Recent Maintenance Work
-----------------------
This version includes a light refactor only:
- duplicated stone-class building logic in frontend files was reduced,
- repeated backend status-update logic after stone placement was reduced,
- docstrings / function descriptions were added across the main backend and JS files,
- endpoint function names were made clearer on the backend,
- README documentation was added.

Known Limitations
-----------------
- No persistent storage or database.
- No automated tests yet.
- Backend logic is concentrated in one file (`quarto.py`), which is workable for a
  small study project but would usually be split into multiple modules in a larger app.
- PvP game flow depends on action markers (`player1_action`, `player2_action`) sent
  from the frontend.

Suggested Next Steps
--------------------
When you have more time, the most natural improvements would be:
- split backend into separate modules (models, schemas, API routes),
- add validation for invalid board fields or illegal repeated placements,
- add automated tests for game logic,
- persist games in a database or cache,
- improve error messages shown on the frontend.
