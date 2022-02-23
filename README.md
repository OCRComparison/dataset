## How to Compare OCR Tools: Tesseract OCR vs Amazon Textract vs Azure OCR vs Google OCR

This is the code to download the FUNSD dataset and extract the dataset used for the OCR comparison.

### Download FUNSD Dataset

wget https://guillaumejaume.github.io/FUNSD/dataset.zip -O dataset.zip

### Unzip FUNSD Dataset

unzip dataset.zip -d ./FUNSD/

### Extraction of the dataset for the OCR comparison

python extract_dataset.py ./FUNSD/ ./OCRDataset/
