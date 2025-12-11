import os
import numpy as np
import time
from selenium.webdriver.common.by import By
import tensorflow as tf
import subprocess
from selenium.webdriver.common.action_chains import ActionChains
import base64

from lib.connect_to_browser import connect_to_browser
from lib.board_cutter import cut_board

TARGET_URL = "https://sudoku.com"

MODEL_PATH = "bin/sudoku_model.keras"
CLASSES_PATH = "bin/classes.txt"
IMG_SIZE = (28, 28)

# Global variables for cash (Singleton)
_model = None
_class_names = None

def load_model():
    """Load the models and classes only once"""
    global _model, _class_names
    if _model is not None:
        return # Already loaded

    # 1. Configure GPU to not crash
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus: tf.config.experimental.set_memory_growth(gpu, True)
        except: pass

    print("🧠 Loading neural network...")
    
    # 2. Load model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found in: {MODEL_PATH}")
    _model = tf.keras.models.load_model(MODEL_PATH)
    
    # 3. Load classes
    if not os.path.exists(CLASSES_PATH):
        raise FileNotFoundError(f"Classes folder not found in: {CLASSES_PATH}")
    
    with open(CLASSES_PATH, "r") as f:
        # Lê linhas e remove o \n
        _class_names = [line.strip() for line in f.readlines()]
    
    print(f"✅ Model ready! {_class_names} known")
    
def read_cell(image_path):
    # Initialize model
    if _model is None:
        load_model()

    try:
        # 1. Load and preprocess the image
        img = tf.keras.utils.load_img(image_path, target_size=IMG_SIZE, color_mode='grayscale')
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        # 2. Inference
        predictions = _model.predict(img_array, verbose=0)
        
        # 3. Interpret
        score = predictions[0]
        class_idx = np.argmax(score)
        class_name = _class_names[class_idx]
        
        return class_name
    
    except Exception as e:
        print(f"❌ Error trying to classify {image_path}: {e}")
        return "error"


def solve_loop():
    driver = connect_to_browser()
    #driver.maximize_window()
    
    if not os.path.exists("data/current_board"):
        os.makedirs("data/current_board")
        print(f"📁 Created data/current_board folder.")

    while True:
        try:
            print("Loading new game...")
            
            # 1. Load page
            driver.get(TARGET_URL)
            time.sleep(1)
            
            # 2. Get board element
            board_element = driver.find_element(By.CSS_SELECTOR, "#game canvas")
            canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", board_element)
            img_binary = base64.b64decode(canvas_base64)

            # 3. Save board
            with open('data/current_board/board.png', 'wb') as f:
                f.write(img_binary)
                
        except Exception as e:
            print(f"❌ Failed: {e}")
            time.sleep(2)
            continue

        cut_board("data/current_board", "data/current_board/board.png", "cell")
        board = ['0']*81
        for i in range(81):
            result = read_cell(f"data/current_board/cell_{i+1:02d}.png")
            if(result != "empty"):
                board[i] = result.split("_")[-1]
        board_string = "".join(board)
        print(f"📥 Original: {board_string}")
        print("🧠 Solving...")
        processo = subprocess.run(
            ["./bin/solver", board_string],
            capture_output=True,
            text=True
        )
        solved_string = processo.stdout.strip()
        
        if "IMPOSSIBLE" in solved_string or len(solved_string) != 81:
            print(f"❌ C++ Solver error: {solved_string}")
            continue

        print(f"✅ Solved: {solved_string}")
        
        # Canvas dimensions
        size = board_element.size
        w = size['width']
        h = size['height']
        cell_w = w / 9
        cell_h = h / 9

        for i in range(81):
            if board_string[i] == '0':
                correct_number = solved_string[i]
                
                # Convert index to collumn and row position
                collumn = i % 9
                row = i // 9
                
                # 1. Coordinate of the cell's center
                x_center = (collumn * cell_w) + (cell_w / 2)
                y_center = (row * cell_h) + (cell_h / 2)
                
                # 2. Shift based on the Canvas center
                # Selenium (0,0) = Canvas (w/2, h/2)
                x_offset = x_center - (w / 2)
                y_offset = y_center - (h / 2)
                
                try:
                    # 1. Point and click
                    (
                        ActionChains(driver)
                        .move_to_element_with_offset(board_element, x_offset, y_offset)
                        .click()
                        .perform()
                    )
                    time.sleep(0.01)

                    # 2. Type
                    (
                        ActionChains(driver)
                        .send_keys(correct_number)
                        .perform()
                    )
                    time.sleep(0.01)
                    
                except Exception as e:
                    print(f"❌ Error on cell {i}: {e}")
        print("✅ Board completed!")

if __name__ == "__main__":
    solve_loop()