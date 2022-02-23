Download FUNSD Dataset

wget https://guillaumejaume.github.io/FUNSD/dataset.zip -O dataset.zip

Unzip FUNSD Dataset

unzip dataset.zip -d ./FUNSD/

Extraction of the dataset for the OCR comparison

python extract_dataset.py ./FUNSD/ ./OCRDataset/