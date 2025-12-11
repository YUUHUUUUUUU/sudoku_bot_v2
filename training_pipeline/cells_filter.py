import os
import shutil
import easyocr
import numpy as np
from PIL import Image

# Configuring paths
INPUT_FOLDER = "data/cells"
OUTPUT_FOLDER = "data/train"

def classify_cells():

    # Load EasyOCR
    print(f"🚀 Loading EasyOCR...")
    reader = easyocr.Reader(['en'], gpu=True, verbose=False)

    cells = sorted([f for f in os.listdir(INPUT_FOLDER)])
    total = len(cells)
    
    print(f"🧠 Starting labeling of {total} cells...")

    stats = {"empty": 0, "ocr_success": 0}

    for i, filename in enumerate(cells):
        path = os.path.join(INPUT_FOLDER, filename)
        
        try:
            img = Image.open(path)
            arr = np.array(img, dtype=int)
            
            # Detect empty cells looking for black pixells
            black_pixels = score = np.sum(arr == 0)
            destination_class = "empty"

            if black_pixels:
                # Congigure the model to search for digits
                results = reader.readtext(path, 
                                        allowlist='123456789',
                                        text_threshold=0, 
                                        low_text=0.3,
                                        mag_ratio=1.5)
                
                # Select the digit with best score
                best_match = max(results, key=lambda x: x[2])
                text = best_match[1]
                
                destination_class = f"number_{text}"
                stats["ocr_success"] += 1
            else:
                stats["empty"] += 1

            # Copy to the destination folder
            shutil.copy(path, os.path.join(OUTPUT_FOLDER, destination_class, filename))

            # Progress log
            if i % 100 == 0:
                print(f"[{i}/{total}] Processing... (Empty: {stats['empty']} | Digits: {stats['ocr_success']})")

        except Exception as e:
            print(f"❌ Error in {filename}: {e}")

    print("-" * 30)
    print("🏆 Finished classifying!")
    print(f"⚪ Empty cells: {stats['empty']}")
    print(f"🔢 Digits: {stats['ocr_success']}")

if __name__ == "__main__":
    classify_cells()