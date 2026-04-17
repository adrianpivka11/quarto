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
