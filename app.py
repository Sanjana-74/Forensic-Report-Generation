import streamlit as st
from datetime import datetime
from src.coordinator import run_full_case
st.set_page_config(page_title="Forensic AI Report Generator", layout="wide")

# --- SIDEBAR: Case Information ---
with st.sidebar:
    st.title("📁 Case Management")
    case_name = st.text_input("Case Name", value=f"Investigation_{datetime.now().strftime('%Y%m%d')}")
    investigator = st.text_input("Lead Investigator", value="Sanjana")
    st.divider()
    st.info("This tool performs Hybrid Vector Analysis and LLM Reasoning to identify digital evidence.")

# --- MAIN UI ---
st.title("🔍 Digital Forensic Intelligence Dashboard")
st.write("Upload evidence files (Images, CSV, TXT, JSON) to begin the automated triage.")

# 1. File Uploader
uploaded_files = st.file_uploader(
    "Drag and Drop Evidence Here", 
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg', 'csv', 'txt', 'json']
)

# 2. Execution Button
if st.button("🚀 Start Full-Pipeline Analysis"):
    if not uploaded_files:
        st.warning("Please upload at least one evidence file.")
    else:
        with st.status("🕵️ Detective at work...", expanded=True) as status:
            st.write("Extracting and Cleaning data...")
            # We pass the case info and files to the coordinator
            final_report, pdf_path = run_full_case(case_name, investigator, uploaded_files)
            
            status.update(label="✅ Investigation Complete!", state="complete", expanded=False)
        
        # 3. DISPLAY THE RESULTS
        st.subheader("📊 Forensic Findings")
        st.markdown(final_report)
        
        # 4. DOWNLOAD THE OFFICIAL PDF
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Official Report",
                data=f,
                file_name=f"{case_name}_Report.pdf",
                mime="application/pdf"
            )