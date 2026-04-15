import os
from src.extractor import get_text_from_file
from src.cleaner import clean_text
from src.analyzer import analyze_forensic_workload

# --- FINAL BOSS PATH LOGIC ---
# This finds the directory where THIS script (test.py) lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# This creates the full path to day1.png inside the same folder
IMAGE_PATH = os.path.join(BASE_DIR, "day1.png")
# ------------------------------

def run_full_pipeline():
    # 1. Check if the file actually exists before starting
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ CRITICAL ERROR: Could not find image at {IMAGE_PATH}")
        print(f"Current Working Directory: {os.getcwd()}")
        return

    # 2. Extraction
    print(f"👀 Step 1: Extracting text from {os.path.basename(IMAGE_PATH)}...")
    with open(IMAGE_PATH, "rb") as f:
        raw_bytes = f.read()
    
    raw_text = get_text_from_file(IMAGE_PATH, raw_bytes)
    
    # 3. Cleaning
    print("🧹 Step 2: Cleaning OCR noise...")
    clean_output = clean_text(raw_text)
<<<<<<< HEAD
=======
    print("--- DEBUG: Day 2 Cleaning Result ---")
    print(clean_output[:100] + "...") 
    print("------------------------------------\n")
>>>>>>> main
    
    # 4. Analysis
    print("🧠 Step 3: Performing Hybrid Forensic Analysis...")
    evidence_set = {os.path.basename(IMAGE_PATH): clean_output}
    final_report = analyze_forensic_workload(evidence_set)
    
    print("\n" + "="*50)
    print("FINAL FORENSIC REPORT")
    print("="*50)
    print(final_report)

if __name__ == "__main__":
    run_full_pipeline()
<<<<<<< HEAD
# After Step 2 (Cleaning)
    print("--- DEBUG: Day 2 Cleaning Result ---")
    #print(clean_output[:100] + "...") # Shows first 100 characters of clean text
    print("------------------------------------\n")
=======
>>>>>>> main
