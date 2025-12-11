#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}      SUDOKU AI - FACTORY RESET          ${NC}"
echo -e "${BLUE}=========================================${NC}"

echo -e "${RED}WARNING: This will delete generated data in 'bin', 'data' and 'training_pipeline'.${NC}"
echo -e "You have 3 seconds to cancel (Ctrl+C)..."
sleep 1
echo -n "3... "
sleep 1
echo -n "2... "
sleep 1
echo "1... Executing."
echo ""

# 1. Clean BIN folder (Files only, keep folder)
if [ -d "bin" ]; then
    echo -e "${YELLOW}[1/3] Cleaning 'bin' folder...${NC}"
    find bin -type f -delete
    echo -e "${GREEN}Cleaned files inside 'bin'.${NC}"
else
    echo -e "${YELLOW}[1/3] 'bin' folder not found. Skipping.${NC}"
fi
sleep 2

# 2. Clean DATA folder (Files only, keep folder structure)
if [ -d "data" ]; then
    echo -e "\n${YELLOW}[2/3] Cleaning 'data' folder...${NC}"
    find data -type f -delete
    echo -e "${GREEN}Cleaned files inside 'data'.${NC}"
else
    echo -e "\n${YELLOW}[2/3] 'data' folder not found. Skipping.${NC}"
fi
sleep 2

# 3. Clean specific Training Graphs only
echo -e "\n${YELLOW}[3/3] Cleaning training graphs...${NC}"

# Only delete the specific outputs in the pipeline folder
rm -f training_pipeline/confusion_matrix.png
rm -f training_pipeline/training_results.png
rm -f training_pipeline/model_validation.png

echo -e "${GREEN}Deleted graphs in 'training_pipeline'.${NC}"
sleep 2

echo -e "\n${BLUE}=========================================${NC}"
echo -e "${GREEN}       REFRESH COMPLETE                  ${NC}"
echo -e "${BLUE}=========================================${NC}"