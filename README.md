
# Bio-Inspired Flocking Simulation 🐦🌟

Welcome to the Bio-Inspired Flocking Simulation project! This simulation replicates advanced flocking behaviors inspired by biological principles, implemented in Python using Pygame.

<p align="center">
<img src="https://github.com/Rishit-katiyar/Bio-inspired-Flocking-Simulation/assets/167756997/891cca96-c704-4f09-9253-99bf45c922dd" alt="Flocking Simulation" width="400" height="300">
</p>

## test_code gif:

<p align="center">
<img src="https://github.com/Rishit-katiyar/Bio-inspired-Flocking-Simulation/assets/167756997/991f6f96-b260-429e-a197-912118c3edee" alt="Flocking Simulation" width="400" height="300">
</p>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project aims to simulate the collective motion of entities (boids) that exhibit behaviors like alignment, cohesion, and separation, similar to flocks of birds or schools of fish. It incorporates advanced features such as dynamic obstacles, predator-prey interactions, and user-controlled elements for visualization.

## Features

- **Advanced Flocking Behaviors**: Includes alignment, cohesion, and separation algorithms.
- **Dynamic Elements**: Obstacles and predators with interactive behaviors.
- **Energy and Hunger Dynamics**: Boids and predators have energy levels that affect their behaviors.
- **User Interaction**: Control elements interactively using mouse and keyboard inputs.
- **Visual Simulation**: Real-time visualization using Pygame for an immersive experience.

## Installation

### Prerequisites

Ensure you have the following installed before proceeding:

- Python (>= 3.6)
- Pygame library

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/bio-inspired-flocking-simulation.git
   cd bio-inspired-flocking-simulation
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   # On Windows:
   # .\venv\Scripts\activate
   # On macOS/Linux:
   # source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the simulation**:

   ```bash
   python main.py
   ```

## Usage

- Left-click to select and drag boids, obstacles, and predators.
- Spacebar to add new boids.
- 'O' key to add new obstacles.
- 'P' key to add new predators.

Experiment with different settings and observe how the flocking behavior adapts to obstacles and predators in real-time!

## Contributing

Contributions are welcome! If you want to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/improvement`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature/improvement`).
6. Create a new Pull Request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
