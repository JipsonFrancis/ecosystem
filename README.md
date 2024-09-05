# 🌿 EcoSystem: Reforesting the Desert Game 🌍

**EcoSystem** is an educational 2D simulation game built using Python and Pygame. The objective of the game is to reforest a desert by planting roses, finding water, and improving the environment. As players plant more roses, they will reduce CO₂ emissions and ultimately transform the desert into a forested area. The game showcases the importance of water and plant life in transforming barren lands into green ecosystems.

---

## 🎮 Features

- **Player Movement**: Move the player left, right, up, and down to explore the desert.
- **Planting Mechanic**: Find water sources, and plant roses to green the desert.
- **Game States**: The game starts in a desert environment and transitions to a forested area once enough plants are grown.
- **Dynamic Environment**: The game environment shifts between desert and forest states based on player actions.
- **Interactive UI**: Visual indicators of the environment’s health and instructions on how to interact with the world.

---

## 🛠️ Object-Oriented Design

The game has been refactored using Object-Oriented Programming (OOP) principles to improve modularity and maintainability:

### 1. **Game Class**
   - Manages the overall game loop, rendering, and event handling.
   - Handles transitions between different game states (Desert and Forested).

### 2. **Player Class**
   - Handles player movement and interactions (e.g., planting roses).
   - Animates player actions using sprite sheets.

### 3. **Rose Class**
   - Represents a rose planted by the player.
   - Draws the rose on the screen at random positions.

### 4. **Background Class**
   - Manages and renders the background for different game states.
   - Supports desert and forested backgrounds with layers for smoke and clouds.

### 5. **WaterSource Class**
   - Handles the discovery of water wells in the desert.
   - Animates water flow when a well is found, helping the player plant roses.

---

## 📖 How to Play

1. **Move**: Use arrow keys to move the player.
   - **Left/Right**: Move the player horizontally.
   - **Up/Down**: Move the player vertically.
   
2. **Find Water**: Press `H` to dig for water.
   
3. **Plant Roses**: Once you've found water, press `P` to plant roses and reduce CO₂ emissions.
   
4. **Transform the Desert**: Plant enough roses to change the game state from desert to forest!

---

## 💡 Game Mechanics

- **Desert Health**: The desert's health starts at 60% and decreases as long as there's smoke in the environment. Plant roses and find water to restore the desert’s health.
- **Cooling Down**: After each rose is planted, there is a short cooldown before the next rose can be planted.
- **Water Sources**: Water is crucial to planting, and it must be found by digging (press `H`).

---

## 📦 Dependencies

- [Pygame](https://www.pygame.org/) - A cross-platform set of Python modules designed for writing video games.

---

## 🚀 Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/eco-system-game.git
