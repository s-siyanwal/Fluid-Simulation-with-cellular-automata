# Fluid-Simulation-with-cellular-automata
This is a simulation of water using cellular automata and pygame to render the simulation.

Each cell of a 50x50 grid is air, solid ground, or holds some mass of water. Every frame, water
flows **down** first, then **left/right** to equalize with neighbours, and finally **up** when a cell
is compressed (holds more than its neighbour above). Slight compression lets pressure push water
up through connected vessels (U-tubes). Deeper water is drawn in darker blue.

## Run
```
pip install -r requirements.txt
python water_sim.py
```
A prebuilt Windows build, `water_sim.exe`, is also included.

## Controls
| Input | Action |
|---|---|
| Left click / drag | Add water |
| Right click / drag | Place a solid block |
| Middle click / drag | Erase (turn the cell back into air) |
| Space | Pause / resume |
| C | Clear all water and blocks |
| Esc | Quit |
