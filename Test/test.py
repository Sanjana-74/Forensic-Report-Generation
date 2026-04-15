import os
import json
from src.extractor import get_text_from_file
from src.cleaner import clean_text
from src.analyzer import analyze_forensic_workload

# --- DYNAMIC PATH LOGIC ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: Ensure the 'D' is capitalized to match your file: Day1.png
IMAGE_PATH = os.path.join(BASE_DIR, "Day1.png") 
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")
STANDARD_PATH = os.path.join(DATA_DIR, "standard.json")

def run_full_evaluation():
    # 0. File Check
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ CRITICAL ERROR: Could not find image at {IMAGE_PATH}")
        return

    print("🚀 STARTING FULL FORENSIC PIPELINE EVALUATION\n")

    # --- DAY 1: EXTRACTION ---
    print("👀 [DAY 1] Extraction: Pulling raw text from evidence...")
    with open(IMAGE_PATH, "rb") as f:
        raw_bytes = f.read()
    
    # Passing "Day1.png" as the filename so the router knows it's an image
    raw_text = get_text_from_file("Day1.png", raw_bytes)
    print(f"--- RAW TEXT ---\n{raw_text}\n" + "-"*20)

    # --- DAY 2: CLEANING ---
    print("\n🧹 [DAY 2] Cleaning: Normalizing OCR noise with LLM...")
    clean_output = clean_text(raw_text)

    print(f"--- CLEANED TEXT ---\n{clean_output}\n" + "-"*20)

    # --- DAY 3: ANALYSIS & RISK ---
    print("\n🧠 [DAY 3] Analysis: Performing Hybrid Vector + LLM Scanning...")
    evidence_set = {"Day1.png": clean_output}

    print("--- DEBUG: Day 2 Cleaning Result ---")
    print(clean_output[:100] + "...") 
    print("------------------------------------\n")
    
    # 4. Analysis
    print("🧠 Step 3: Performing Hybrid Forensic Analysis...")
    evidence_set = {os.path.basename(IMAGE_PATH): clean_output}

    final_report = analyze_forensic_workload(evidence_set)
    
    # --- DAY 4: ACCURACY GRADING ---
    print("\n🎯 [DAY 4] Grading: Comparing AI report to standard.json...")
    
    try:
        with open(STANDARD_PATH, "r") as f:
            standards = json.load(f)
        
        # Look for Day1.png entry in the answer key
        expected = next((item for item in standards if item["file_name"] == "Day1.png"), None)
        
        if expected:
            matches = 0
            total = len(expected["expected_findings"])
            
            print("\n--- ACCURACY CHECKLIST ---")
            for item in expected["expected_findings"]:
                # Check if the AI report mentioned the category or finding phrase
                if item["category"].lower() in final_report.lower():
                    matches += 1
                    print(f"✅ FOUND: {item['category']}")
                else:
                    print(f"❌ MISSED: {item['category']}")

            accuracy_score = (matches / total) * 100
            print(f"\n📈 FINAL MODEL ACCURACY: {accuracy_score:.1f}%")
        else:
            print("⚠️ WARNING: No entry for Day1.png found in standard.json")
    except Exception as e:
        print(f"⚠️ GRADING FAILED: Ensure standard.json is in /data. Error: {e}")

    # --- FINAL DISPLAY ---
    print("\n" + "="*50)
    print("FINAL FORENSIC REPORT (What the user sees)")
    print("="*50)
    print(final_report)

if __name__ == "__main__":

    run_full_evaluation()

