import os
from PIL import Image

def cut_board(EXIT_FOLDER, BOARD_PATH, PREFIX):
    MARGIN = 30
    
    try:
        # Open image with Pillow
        board_img = Image.open(BOARD_PATH)
        total_width, total_height = board_img.size

        # Calculate cells dimensions
        largura_celula = total_width // 9
        cell_height = total_height // 9
        
        # Iterate over 9x9 board
        for line in range(9):
            for row in range(9):
                # Get the upper left coordinate
                left = row * largura_celula
                upper = line * cell_height
                
                # Get the bottom right coordinate
                right = left + largura_celula
                lower = upper + cell_height
                
                # Apply margins
                left += MARGIN
                upper += MARGIN
                right -= MARGIN
                lower -= MARGIN

                # Crop based on the coordinates
                celula_img = board_img.crop((left, upper, right, lower))
                
                celula_img = celula_img.convert('L').point(lambda p: 255 if p > 128 else 0, mode='L')
                
                pos = f"{9*(line) + row + 1:02d}"
                file_name = f"{PREFIX}_{pos}.png"
                file_path = os.path.join(EXIT_FOLDER, file_name)
                
                celula_img.save(file_path)
                
        print(f"✅ {BOARD_PATH} processed.")

    except Exception as e:
        print(f"❌ Error processing {BOARD_PATH}: {e}")