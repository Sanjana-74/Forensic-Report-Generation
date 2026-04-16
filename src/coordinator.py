import os
from datetime import datetime
from src.extractor import get_text_from_file
from src.cleaner import clean_text
from src.analyzer import analyze_forensic_workload
from src.generator import create_pdf_report

def run_full_case(case_id, investigator, uploaded_files):
    """The master pipeline that runs Day 1 through Day 4."""
    
    processed_evidence = {}
    
    for uploaded_file in uploaded_files:
        # 1. Extraction (Day 1)
        file_bytes = uploaded_file.read()
        raw_text = get_text_from_file(uploaded_file.name, file_bytes)
        
        # 2. Cleaning (Day 2)
        cleaned_text = clean_text(raw_text)
        
        # Add to the workload for the analyzer
        processed_evidence[uploaded_file.name] = cleaned_text

    # 3. Analysis (Day 3 & 4)
    # This calls your Vector Matching + LLM Reasoning
    final_report = analyze_forensic_workload(processed_evidence)

    # 4. Report Generation (Day 5)
    metadata = {
        "id": case_id,
        "name": investigator,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    pdf_path = create_pdf_report(metadata, final_report)

    return final_report, pdf_path