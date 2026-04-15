import pandas as pd
import easyocr
from PIL import Image
import io

# We initialize the reader once to save memory
# 'en' tells it to look for English text
reader = easyocr.Reader(['en'])
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
    """The 'Router' that picks the right tool based on file type."""
    ext = file_name.split('.')[-1].lower()

    if ext in ['png', 'jpg', 'jpeg']:
        return extract_from_image(file_bytes)
    elif ext == 'csv':
        return extract_from_csv(file_bytes)
    elif ext == 'json':
        return extract_from_json(file_bytes)
    elif ext == 'txt':
        return extract_from_txt(file_bytes)
    else:
        return "Unsupported file format."