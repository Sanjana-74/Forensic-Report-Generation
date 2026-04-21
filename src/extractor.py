import pandas as pd
import easyocr
from PIL import Image
import io
import json
import hashlib

# We initialize the reader once to save memory
# 'en' tells it to look for English text
reader = easyocr.Reader(['en'])
def calculate_sha256(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()
def extract_from_txt(file_bytes):
    """Reads plain text files."""
    # .decode('utf-8') turns the raw bytes into a human-readable string
    return file_bytes.decode('utf-8')

def extract_from_image(file_bytes):
    """Reads text from screenshots or photos."""
    # EasyOCR can read the 'file_bytes' directly! 
    # We don't need to use PIL (Image.open) here.
    results = reader.readtext(file_bytes, detail=0) 
    return " ".join(results)

def extract_from_csv(file_bytes):
    """Reads data from CSV files and converts it to a text block."""
    df = pd.read_csv(io.BytesIO(file_bytes))
    return df.to_string(index=False)

def extract_from_json(file_bytes):
    """Reads data from JSON files."""
    data = json.loads(file_bytes.decode('utf-8'))
    return json.dumps(data, indent=2)

def get_text_from_file(file_name, file_bytes):
    """The 'Router' that now correctly returns BOTH text and hash."""
    ext = file_name.split('.')[-1].lower()
    file_hash = calculate_sha256(file_bytes)
    
    # Store the result in a variable instead of returning immediately
    if ext in ['png', 'jpg', 'jpeg']:
        text = extract_from_image(file_bytes)
    elif ext == 'csv':
        text = extract_from_csv(file_bytes)
    elif ext == 'json':
        text = extract_from_json(file_bytes)
    elif ext == 'txt':
        text = extract_from_txt(file_bytes)
    else:
        text = "Unsupported file format."
        
    # Now return both values as a tuple
    return text, file_hash