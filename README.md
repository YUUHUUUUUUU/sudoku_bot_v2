# 🧩 Hybrid AI Sudoku Solver

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)
![C++](https://img.shields.io/badge/C++-17-red?style=flat&logo=cplusplus)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=flat&logo=tensorflow)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=flat&logo=opencv)

A full-stack autonomous bot that visually solves online Sudoku puzzles in real-time.

This project implements a **Hybrid Architecture**: it uses **Python (Computer Vision)** to "read" the screen pixels and **C++** for high-performance algorithms to "solve" the logic, bridging the two languages via standard I/O streams.

![Image](https://github.com/user-attachments/assets/5d09140c-55c1-464b-a4d1-a4f74a93a9bd)

## 🏗️ Architecture

The system operates in two distinct phases:

### 1. The Training Pipeline (MLOps)

An automated pipeline that generates its own dataset from the live website to train the neural network.

* **Scraping:** Opens the browser via Selenium and captures raw board images.
* **Slicing:** Cuts the board into 81 individual cells using OpenCV.
* **Labeling (Weak Supervision):** Uses **Ink Density Heuristics** to filter empty cells and **EasyOCR (PyTorch)** to auto-label the digits.
* **Training:** Trains a Convolutional Neural Network (LeNet-5 architecture) to recognize digits with 100% accuracy.

### 2. The Runtime Bot

The "Production" loop that runs in real-time using the trained brain.

1.  **Eye:** Selenium captures the HTML Canvas state.
2.  **Brain (Visual):** The trained CNN classifies the 81 cells into a numerical matrix.
3.  **Brain (Logic):** The matrix is piped to a compiled **C++ executable** (`bin/solver`) which solves the puzzle using Recursive Backtracking.
4.  **Hand:** Selenium calculates screen coordinates and simulates human-like clicks to fill the board.

---

## 📂 Project Structure

```text
.
├── bin/                     # Compiled artifacts (C++ Solver, Keras Model/ONNX)
├── data/                    # Generated Datasets (Raw boards, Processed cells)
├── lib/                     # Shared Python modules (Browser connection, Image cutter)
├── training_pipeline/       # Scripts for MLOps (Generation, Filtering, Training)
│   ├── cells_generator.py   # Scrapes raw data
│   ├── cells_filter.py      # Auto-labels data with EasyOCR
│   └── cnn_trainer.py       # Trains the CNN
├── main.py                  # The main bot orchestration script
├── solver.cpp               # High-performance C++ backtracking algorithm
├── requirements.txt         # Python dependencies (Pinned versions)
├── run_training_pipeline.sh # Script to generate data and train model
├── run_bot.sh               # Script to compile and run the bot
└── refresh.sh               # Nuke script to clean all generated data
```

## 🚀 Getting Started

This project is optimized for **Linux** environments.

### Prerequisites

* **Python 3.10+**
* **Google Chrome**
* **G++ Compiler** (for the solver)

```bash
# Ubuntu / Debian / Linux Mint
sudo apt update
sudo apt install g++ google-chrome-stable
```

## 🛠️ Installation & Usage

I have provided automation scripts to handle the entire lifecycle.

### 1. Train the Brain (First Run)

If you are running this for the first time, you need to generate the dataset and train the model. This script will open Chrome, play 100 games, learn the digits, and save the model to `bin/`.

```bash
chmod +x run_training_pipeline.sh
./run_training_pipeline.sh
```

### 2. Run the Bot
This script compiles the C++ solver (ensuring max performance), connects to the browser, and starts solving puzzles endlessly.

```bash
chmod +x run_bot.sh
./run_bot.sh
```

### 3. Factory Reset
If you want to clear all datasets, models, and logs to start fresh:

```bash
chmod +x refresh.sh
./refresh.sh
```

### 4. Running it after the setup
If you want to open the debug tab and run the model separatelly after the first run:

```bash
# Open the tab
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug_sudoku" --incognito --window-size=1200,800 "https://sudoku.com/easy/" &> /dev/null &

# Run the program
python main.py
```

## 🧠 Technical Highlights

### The Convolutional Neural Network (CNN)

The model is designed to be lightweight and fast. It includes Data Augmentation layers directly inside the model structure.

* Input: 28x28 Grayscale images.
* Preprocessing: Rescaling (1./255) + Random Rotation/Zoom/Shift.
* Architecture: 3 Convolutional Blocks -> Flatten -> Dense (Relu) -> Dropout (0.2) -> Softmax.
* Result: Robust against browser zoom levels and slight rendering shifts.

### The C++ Integration

Instead of solving the Sudoku in Python (which is slower), the grid is serialized into a string and passed to a C++ binary via subprocess.

* Performance: Solves hard puzzles in milliseconds.
* Algorithm: Recursive Backtracking with optimizations.

### Browser Automation

* Debug Port: The bot launches Chrome with --remote-debugging-port=9222. This allows the Python script to attach/detach from the browser session without killing the window, facilitating debugging.
* Input Simulation: Uses ActionChains to map matrix indices (0..80) to physical (X, Y) screen coordinates relative to the canvas center.

## ⚠️ Disclaimer

This project is for educational purposes only, demonstrating Computer Vision and MLOps concepts. Using bots on public websites may violate their Terms of Service. Use responsibly.