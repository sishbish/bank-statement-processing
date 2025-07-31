from PIL import Image
import pytesseract
import cv2
from pdf2image import convert_from_path
import numpy as np

# convert PDF to images
pages = convert_from_path('/Users/sishirsirugudi/MK Intern Stuff/RN.pdf', dpi=300)

rows, cols = 175, 310

with open("spatial_text.txt", "w") as f:
    for img in pages:
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        data = pytesseract.image_to_data(img, output_type='dict')
        print("data:", data)
        canvas = [[' ' for _ in range(cols)] for _ in range(rows)]

        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            if word and int(data['conf'][i]) > 20:
                x = data['left'][i]
                y = data['top'][i]
                col = x // 16
                row = y // 40
                if row < rows and col < cols - len(word):
                    for j, char in enumerate(word):
                        canvas[row][col + j] = char
        
        for row in canvas:
            f.write(''.join(row) + '\n')
        
    