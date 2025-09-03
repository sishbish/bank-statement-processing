import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import pdf2image

# Load pretrained CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# categories
categories = [
    "a scanned bank statement",
    "a scanned payslip",
    "a P60 tax document",
    "a UK driving license",
    "a UK passport",
    "a visa",
    "anything else"
]


# image = pdf2image.convert_from_path("/Users/sishirsirugudi/Downloads/PP.pdf", dpi=300)
image = Image.open('/Users/sishirsirugudi/MK Intern Stuff/bank files/visa2.jpg')  
# Preprocess inputs
inputs = processor(
    text=categories,
    images=image,
    return_tensors="pt",
    padding=True
)

# Run model
with torch.no_grad():
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # [1, num_categories]
    probs = logits_per_image.softmax(dim=1)

# Get predicted label
pred_idx = probs.argmax().item()
print(f"Predicted class: {categories[pred_idx]}")
print(f"Probabilities: {probs}")