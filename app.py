import streamlit as st
from datetime import datetime
from src.coordinator import run_full_case
import pandas as pd 
import os


st.set_page_config(page_title="Forensic AI Report Generator", layout="wide")

if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'final_report' not in st.session_state:
    st.session_state.final_report=None
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None
# --- SIDEBAR: Case Information ---
with st.sidebar:
    st.title("📁 Case Management")
    case_name = st.text_input("Case Name", value=f"Investigation_{datetime.now().strftime('%Y%m%d')}")
    investigator = st.text_input("Lead Investigator", value="Sanjana")
    st.divider()


    if st.button("🗑️ Clear Current Analysis"):
        st.session_state.final_report = None
        st.session_state.pdf_path = None
        st.rerun()
    st.info("This tool performs Hybrid Vector Analysis and LLM Reasoning to identify digital evidence.")

# --- MAIN UI ---
st.title("🔍 Digital Forensic Intelligence Dashboard")
st.write("Upload evidence files (Images, CSV, TXT, JSON) to begin the automated triage.")
lock_ui = st.session_state.is_processing or st.session_state.final_report is not None
# 1. File Uploader
uploaded_files = st.file_uploader(
    "Drag and Drop Evidence Here", 
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg', 'csv', 'txt', 'json'],
    disabled=lock_ui
)

# 2. Execution Button
if st.button("Generate Report",disabled=lock_ui):
    if not uploaded_files:
        st.warning("Please upload at least one evidence file.")
    else:
        st.session_state.is_processing = True
        st.rerun()
if st.session_state.is_processing and not st.session_state.final_report:   
    with st.status("🕵️ Analyzing Evidence Flow...", expanded=True) as status:
        report, path = run_full_case(case_name, investigator, uploaded_files)
            
        st.session_state.final_report = report
        st.session_state.pdf_path = path
        st.session_state.is_processing = False
        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
    st.rerun()    
        # 3. DISPLAY THE RESULTS
if st.session_state.final_report:
    st.divider()
    st.subheader("📄 Official Investigative Narrative")
    
    # Display the narrative report
    st.markdown(st.session_state.final_report)            
        # 4. DOWNLOAD THE OFFICIAL PDF
    if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Official Report",
                data=f,
                file_name=f"{case_name}_Final_Report.pdf",
                mime="application/pdf"
            )
        try:
            os.remove(st.session_state.pdf_path)
        except:
            pass