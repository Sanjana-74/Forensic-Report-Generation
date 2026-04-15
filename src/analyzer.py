import os
<<<<<<< HEAD
=======
import joblib
>>>>>>> main
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
def analyze_forensic_workload(files_dict):
    """
    Finalized Day 3 Analyzer: Handles multiple files, 
    identifies correlations, and uses robust few-shot examples.
=======
def get_local_risk_prediction(text):
    """Checks the local trained model for a quick risk score."""
    try:
       
        model = joblib.load('src/risk_model.joblib')
        vectorizer = joblib.load('src/vectorizer.joblib')
        
        vector = vectorizer.transform([text])
        prediction = model.predict(vector)[0]
        mapping = {0: "Low", 1: "Medium", 2: "High"}
        return mapping.get(prediction, "Unknown")
    except:
        
        return "Pending Local Training"

def analyze_forensic_workload(files_dict):
    """
    Finalized Day 3 Analyzer: Integrates Local ML flags + LLM Deep Analysis.
>>>>>>> main
    """
    # 1. Self-Healing Client Initialization
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "❌ ERROR: GROQ_API_KEY not found in .env!"
    
    client = Groq(api_key=api_key)

<<<<<<< HEAD
    # 2. Evidence Preparation
    combined_evidence = ""
    for filename, content in files_dict.items():
        combined_evidence += f"=== SOURCE FILE: {filename} ===\n{content}\n\n"

    # 3. The Robust, Universal System Prompt (The one you liked!)
    system_prompt = (
        "You are a Senior Digital Forensic Investigator. Analyze the provided evidence "
        "to identify suspicious activity and cross-file correlations.\n\n"
        
        "### FEW-SHOT EXAMPLES:\n"
        "1. Finding: | Data Integrity | 'Ran sdelete' | Use of secure-overwrite tools. | Critical | logs.txt |\n"
        "2. Finding: | Financial | 'XBT-Wallet-99' | Use of anonymous crypto-wallets. | High | chat.png |\n"
        "3. Finding: | Intellectual Property | 'Copied Source Code' | Unauthorized duplication of assets. | High | cap.jpg |\n"
        "4. Finding: | Secrecy | 'Talk on Signal only' | Moving to encrypted channels. | Medium | email.txt |\n"
        "5. Finding: | Narcotics | 'Packages in blue bin' | Vague language for illicit exchange. | High | chat.png |\n\n"
=======
    # 2. Evidence Preparation (Including Local ML Triage)
    combined_evidence = ""
    for filename, content in files_dict.items():
        # Here we use the local model to get a 'First Opinion'
        local_risk = get_local_risk_prediction(content)
        
        combined_evidence += f"=== SOURCE FILE: {filename} ===\n"
        combined_evidence += f"[LOCAL ML RISK SCORE: {local_risk}]\n"
        combined_evidence += f"CONTENT: {content}\n\n"

    # 3. The Robust, Universal System Prompt
    system_prompt = (
        "You are a Senior Digital Forensic Investigator. Analyze the provided evidence "
        "and the 'LOCAL ML RISK SCORE' to identify suspicious activity.\n\n"
        
        "### FEW-SHOT EXAMPLES:\n"
        "1. Finding: | Secrecy | 'Talk on Signal' | Moving to encrypted channels. | High | chat.png |\n"
        "2. Finding: | Data Integrity | 'Ran sdelete' | Use of secure-overwrite tools. | Critical | logs.txt |\n"
        "3. Finding: | Intellectual Property | 'Copied Source Code' | Unauthorized duplication. | High | cap.jpg |\n\n"
>>>>>>> main
        
        "### OUTPUT FORMAT:\n"
        "Return your findings in a Markdown TABLE, followed by a 'CROSS-FILE CORRELATIONS' section."
    )

    # 4. AI Execution
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
<<<<<<< HEAD
                {"role": "user", "content": f"Analyze this evidence set:\n{combined_evidence}"}
=======
                {"role": "user", "content": f"Analyze this workload:\n{combined_evidence}"}
>>>>>>> main
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Analysis Failed: {e}"