# Bumper-Cars-Simulator

## Overview
A virtual bumper car simulator inspired by the behavior of boids, featuring both single-player and multiplayer modes. Players can control their cars via an OSC (Open Sound Control) interface, with unique features such as NPC cars, customizable player car colors, and sound effects to enhance the gameplay experience.

---

## Features

### Gameplay Modes
- **Single-Player**: Includes NPC cars that react dynamically to the player's actions.
- **Multiplayer**: Allows up to 10 players to compete, with an option to include NPCs.

### Key Functionalities
- **OSC Integration**: Players control their cars via OSC data from `interface.py`.
- **Customizable Car Colors**: Multiplayer mode lets players choose their car color.
- **Physics-Based Interactions**: Cars bounce off each other and display boundaries.
- **Sound Effects**: Realistic audio feedback for car collisions and boundary hits.

---

## Getting Started

### Prerequisites
- Required Libraries: `gui`, `math`, `random`, `osc`, `music`

---

## Controls
- **Movement**: Controlled via OSC input from the `interface.py` script.
- **Multiplayer Configuration**: Enter the desired port number for the car color.

### OSC Port Numbers and Colors
| Port   | Color       |
|--------|-------------|
| 28821  | Red         |
| 28822  | Orange      |
| 28823  | Yellow      |
| 28824  | Lite Green  |
| 28825  | Green       |
| 28826  | Lite Blue   |
| 28827  | Blue        |
| 28828  | Lite Purple |
| 28829  | Purple      |
| 28830  | Pink        |

---

## Code Structure

### Main Components
1. **Platform**: The main game environment where all cars interact.
2. **Player**: Represents a user-controlled car.
3. **NPC**: Represents non-playable cars with autonomous behavior.

### Key Scripts
- `bump_it.py`: Main game logic and entry point.
- `interface.py`: Handles OSC input for car control.
- `gui.py`, `osc.py`, `music.py`: Supporting modules for GUI, OSC, and audio.

---

## Rules and Behavior
The car movements are influenced by three boids-inspired rules:
1. **Separation**: Cars avoid collisions by moving away from nearby cars.
2. **Alignment**: Cars align their velocity with neighboring cars.
3. **Cohesion**: Cars are attracted to a central point.

---

## Future Enhancements
- Integrate a scoring system.
- Implement additional car models and dynamic obstacles.
- Enhance the AI behavior for NPCs.

---

## Audio
### Sound Effects
- **Car Collisions**: `carBonk.wav`
- **Player Collisions**: `playerBonk.wav`
- **Boundary Hits**: `platform.wav`

### Background Music
- `carnival.wav`: Loops throughout gameplay.

---

## Credits
- **Developed by**: Chi Nguyen
- **Inspiration**: Boids simulation
