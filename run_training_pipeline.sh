#!/bin/bash

# Colors for the terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}    SUDOKU AI - TRAINING PIPELINE        ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Environment & Requirements Check
echo -e "\n${YELLOW}[1/4] Checking system health...${NC}"

# A. Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found!${NC}"
    exit 1
fi

# B. Install Python Dependencies
echo -e "Installing/Updating Python libraries..."
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo -e "${RED}Error installing python requirements. Check the logs.${NC}"
    exit 1
fi
echo -e "${GREEN}Python environment OK.${NC}"

# C. Check Google Chrome (Needed for Selenium)
if ! command -v google-chrome &> /dev/null; then
    echo -e "${RED}Error: Google Chrome not found.${NC}"
    echo -e "Please install Chrome to allow Selenium to collect data."
    exit 1
fi
sleep 1

# 2. Chrome Setup (For Data Generation)
echo -e "\n${YELLOW}[2/4] Setting up Google Chrome (Debug Mode)...${NC}"
if lsof -i:9222 -t >/dev/null; then
    echo -e "${GREEN}Chrome is already running on port 9222. Skipping launch.${NC}"
else
    echo -e "Launching new Chrome instance..."
    nohup google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug_sudoku" --incognito --window-size=1200,800 "https://sudoku.com/easy/" &> /dev/null &
    disown
    echo -e "${GREEN}Chrome launched.${NC}"
fi
sleep 2

# 3. Execution Loop
echo -e "\n${YELLOW}[3/4] Running Python Pipeline...${NC}"

echo -e "${BLUE}STEP A: Generating Dataset (Selenium)${NC}"
python3 training_pipeline/cells_generator.py
if [ $? -ne 0 ]; then echo -e "${RED}Failed at Step A.${NC}"; exit 1; fi
echo -e "${GREEN}Dataset generated.${NC}"
sleep 1

echo -e "${BLUE}STEP B: Filtering & Labeling (EasyOCR)${NC}"
python3 training_pipeline/cells_filter.py
if [ $? -ne 0 ]; then echo -e "${RED}Failed at Step B.${NC}"; exit 1; fi
echo -e "${GREEN}Data labeled.${NC}"
sleep 1

echo -e "${BLUE}STEP C: Training CNN Model (TensorFlow)${NC}"
python3 training_pipeline/cnn_trainer.py
if [ $? -ne 0 ]; then echo -e "${RED}Failed at Step C.${NC}"; exit 1; fi
echo -e "${GREEN}Model trained and saved.${NC}"
sleep 1

echo -e "${BLUE}STEP D: Creating Report (TensorFlow)${NC}"
python3 training_pipeline/model_validation.py
if [ $? -ne 0 ]; then echo -e "${RED}Failed at Step D.${NC}"; exit 1; fi
echo -e "${GREEN}Report created.${NC}"
sleep 1

echo -e "\n${BLUE}=========================================${NC}"
echo -e "${GREEN}       TRAINING COMPLETE!                ${NC}"
echo -e "${BLUE}=========================================${NC}"