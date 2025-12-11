#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}       SUDOKU AI - RUNTIME BOT           ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Dependency Check
echo -e "\n${YELLOW}[1/4] Checking Python requirements...${NC}"
# Only installs if missing, suppressing output for cleaner look
pip install -r requirements.txt -q
echo -e "${GREEN}Requirements OK.${NC}"
sleep 2

# 2. C++ Compilation
echo -e "\n${YELLOW}[2/4] Compiling C++ Solver...${NC}"
mkdir -p bin
g++ solver.cpp -o bin/solver -O3
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Solver compiled successfully at bin/solver${NC}"
else
    echo -e "${RED}C++ Compilation Failed.${NC}"
    exit 1
fi
sleep 2

# 3. Chrome Setup
echo -e "\n${YELLOW}[3/4] Checking Google Chrome...${NC}"
if lsof -i:9222 -t >/dev/null; then
    echo -e "${GREEN}Chrome is already running on port 9222. Connecting to existing session.${NC}"
else
    echo -e "Launching new Chrome instance..."
    nohup google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug_sudoku" --incognito --window-size=1200,800 "https://sudoku.com/easy/" &> /dev/null &
    disown
    echo -e "${GREEN}Chrome launched.${NC}"
fi
sleep 2

# 4. Run Main Bot
echo -e "\n${YELLOW}[4/4] Starting Main Bot...${NC}"
echo -e "${BLUE}-----------------------------------------${NC}"
python3 main.py
echo -e "${BLUE}-----------------------------------------${NC}"

echo -e "\n${GREEN}Bot finished execution.${NC}"
echo -e "Chrome window remains open for inspection."