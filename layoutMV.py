import pytesseract
import pdf2image
from PIL import Image
from transformers import LayoutLMv3Processor, LayoutLMv3TokenizerFast, LayoutLMv3FeatureExtractor
from transformers.models.fnet.modeling_fnet import apply_chunking_to_forward
import torch





def process_image(page):
    # Load the LayoutLMv3 processor with built-in OCR
    feature_extractor = LayoutLMv3FeatureExtractor(apply_ocr= True, ocr_lang = "eng")
    tokenizer = LayoutLMv3TokenizerFast.from_pretrained("microsoft/layoutlmv3-base")
    processor = LayoutLMv3Processor(feature_extractor, tokenizer) 

    encoding = processor(
        page,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=512
    )


    features = feature_extractor(page)

    words = features['words'][0] 
    bounding_boxes = features['boxes'][0]
    # print(words [0:100])
    # print(bounding_boxes[0:5]) 

    return {
        'words': words,
        'boxes': bounding_boxes
    }


rows, cols = 175, 310

pages = pdf2image.convert_from_path('/Users/sishirsirugudi/MK Intern Stuff/RN.pdf', dpi=300)
with open("testing.txt", "w") as f:
    for img in pages:
        data = process_image(img)
        canvas = [[' ' for _ in range(cols)] for _ in range(rows)]

        for i in range(len(data['words'])):
            word = data['words'][i].strip()
            x = data['boxes'][i][0]
            y = data['boxes'][i][1]
            col = x // (2*3)
            row = y // (5*3)
            
            if row < rows and col < cols - len(word):
                for j, char in enumerate(word):
                    canvas[row][col + j] = char
        
        for row in canvas:
            f.write(''.join(row) + '\n')
