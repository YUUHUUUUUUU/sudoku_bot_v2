import os
import sys
import time
from selenium.webdriver.common.by import By
import base64

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from lib.connect_to_browser import connect_to_browser
from lib.board_cutter import cut_board

NUMBER_OF_BOARDS = 10
BOARDS_FOLDER = "data/boards"
CELLS_FOLDER = "data/cells"

def generate_cells():
    driver = connect_to_browser()
    driver.maximize_window() 
    
    if not os.path.exists(BOARDS_FOLDER):
        os.makedirs(BOARDS_FOLDER)
        print(f"📁 Created '{BOARDS_FOLDER}' folder.")
    if not os.path.exists(CELLS_FOLDER):
        os.makedirs(CELLS_FOLDER)
        print(f"📁 Created '{CELLS_FOLDER}' folder.")

    print(f"📸 Starting the processing of {NUMBER_OF_BOARDS} boards...")
    
    board_element = driver.find_element(By.ID, "game")

    for i in range(1, NUMBER_OF_BOARDS + 1):
        try:
            print(f"🔄 [{i}/{NUMBER_OF_BOARDS}] Loading new game...")
            
            # 1. Load the page
            driver.get("https://sudoku.com/easy/")
            time.sleep(1)
            
            # 2. Fetch the canva
            board_element = driver.find_element(By.CSS_SELECTOR, "#game canvas")
            canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", board_element)
            img_binary = base64.b64decode(canvas_base64)

            # 3. Save the board
            with open(f"{BOARDS_FOLDER}/sudoku_{i:03d}.png", 'wb') as f:
                f.write(img_binary)
            
            # 4. Break boards into cells
            cut_board(CELLS_FOLDER, f"{BOARDS_FOLDER}/sudoku_{i:03d}.png", f"cell_{i:03d}")

        except Exception as e:
            print(f"❌ Error on iteration {i}: {e}")
            continue

    print("✅ Boards saved!")
    
if __name__ == "__main__":
    generate_cells()