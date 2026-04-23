import streamlit as st
from datetime import datetime
from src.coordinator import run_full_case
import pandas as pd 
import os


st.set_page_config(page_title="Forensic AI Report Generator", layout="wide")

if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'show_main' not in st.session_state:
    st.session_state.show_main = False
if 'is_processing' not in st.session_state:
    st.session_state.is_processing = False
if 'final_report' not in st.session_state:
    st.session_state.final_report=None
if 'pdf_path' not in st.session_state:
    st.session_state.pdf_path = None

if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0
bg_color = "#0a192f"
sidebar_color = "#112240"
card_color = "#172a45"
text_color = "#ccd6f6"
accent_color = "#00d1ff"

# --- GLOBAL CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    
    /* Remove link symbols on hover */
    [data-testid="stHeaderActionElements"], .header-anchor {{ display: none !important; }}
    
    /* Home Section - Massive Hello */
    .hero-text {{
        font-size: 6rem;
        font-weight: 800;
        text-align: center;
        margin-top: 50px;
        color: {accent_color};
    }}
    .sub-hero {{
        text-align: center;
        font-size: 1.4rem;
        opacity: 0.8;
        line-height: 1.8;
        margin-bottom: 30px;
    }}
    .scroll-indicator {{
        text-align: center;
        color: {accent_color};
        font-weight: bold;
        margin-bottom: 100px;
    }}
    
    /* The Square Dotted Uploader */
    [data-testid="stFileUploadDropzone"] {{
        background-color: {card_color};
        border: 2px dashed {accent_color} !important;
        border-radius: 20px;
        width: 400px !important;
        height: 400px !important;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: auto;
    }}
    
    /* STRICTLY hide the default file list below the uploader */
    [data-testid="stFileUploaderFileData"] {{ display: none !important; }}
    
    /* Forensic Card for Report */
    .forensic-card {{
        background-color: {card_color};
        padding: 40px;
        border-radius: 15px;
        border-left: 10px solid {accent_color};
        box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 1. THE POP-UP DIALOG (USER LOGIN) ---
@st.dialog("Access Terminal")
def login_dialog():
    st.write("Welcome. Please enter your name to access the dashboard.")
    name = st.text_input("User Name", placeholder="Type here...")
    if st.button("Enter Dashboard"):
        st.session_state.user_name = name if name.strip() else "User"
        st.session_state.show_main = True
        st.rerun()

if not st.session_state.show_main:
    login_dialog()
    st.stop()

# --- 2. HOME SECTION ---
st.markdown(f'<div class="hero-text">Hello, {st.session_state.user_name}</div>', unsafe_allow_html=True)

# THE THREE LINES YOU WANTED BACK:
st.markdown(f"""
    <div class="sub-hero">
        This platform utilizes Neural Embedding and Large Language Models to <br>
        reconstruct digital evidence narratives with high precision. <br>
        Automating the triage process allows investigators to focus on high-level strategy.
    </div>
    <div class="scroll-indicator">Scroll below to begin analysis ↓</div>
""", unsafe_allow_html=True)

st.divider()

# --- 3. WORKSPACE SECTION ---
with st.sidebar:
    st.title("📁 Case Details")
    case_id = st.text_input("Case ID", value=f"FORENSIC-{datetime.now().strftime('%m%d%y')}")
    lead_investigator = st.text_input("Lead Investigator", value=st.session_state.user_name)

st.header("🔍 Evidence Intake")
col1, col2 = st.columns([1, 1])

with col1:
    lock_ui = st.session_state.is_processing or st.session_state.final_report is not None
    uploaded_files = st.file_uploader(
        "Drop Evidence Here", 
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg', 'csv', 'txt', 'json'],
        disabled=lock_ui,
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}" # Key for resetting
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Process Pipeline", disabled=lock_ui, use_container_width=True):
        if not uploaded_files:
            st.warning("No data provided.")
        else:
            st.session_state.is_processing = True
            st.rerun()

with col2:
    st.subheader("📁 Inventory (Uploaded Files)")
    if uploaded_files:
        for f in uploaded_files:
            st.markdown(f"""
                <div style='background:{card_color}; padding:12px; border-radius:8px; margin-bottom:8px; border:1px solid {accent_color}44'>
                    ✅ <b>{f.name}</b> <br>
                    <span style='font-size:0.8rem; opacity:0.6;'>Size: {(f.size/1024):.1f} KB</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Awaiting evidence for analysis...")

# --- 4. CORE LOGIC ---
if st.session_state.is_processing and not st.session_state.final_report:
    with st.status("🕵️ Executing Forensic Triage...", expanded=True) as status:
        report, path = run_full_case(case_id, lead_investigator, uploaded_files)
        st.session_state.final_report = report
        st.session_state.pdf_path = path
        st.session_state.is_processing = False
        status.update(label="✅ Analysis Complete!!", state="complete")
    st.rerun()

# --- 5. REPORT & ACTION BUTTONS ---
if st.session_state.final_report:
    st.divider()
    st.markdown(f"""
        <h2 style='color: {accent_color}; letter-spacing: 1px; margin-bottom: -10px;'>
            📄 Official Investigative Narrative
        </h2>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="forensic-card">{st.session_state.final_report}</div>', unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Spaced out Buttons
    btn_col1, spacer, btn_col2 = st.columns([1, 2, 1])
    
    with btn_col1:
        if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
            with open(st.session_state.pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name=f"{case_id}_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            try: os.remove(st.session_state.pdf_path)
            except: pass

    with btn_col2:
        # RESET WORKSPACE ONLY (Keeps user_name and show_main)
        if st.button("🗑️ Clear Evidence", use_container_width=True):
            st.session_state.final_report = None
            st.session_state.pdf_path = None
            st.session_state.is_processing = False
            st.session_state.uploader_key += 1 # Increments key to clear uploader widget
            st.rerun()
