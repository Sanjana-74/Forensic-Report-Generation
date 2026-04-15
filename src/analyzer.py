import os
import joblib
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def get_vector_finding(text_content):
    """
    Local Triage: Uses Vector Similarity to check our 75-row 
    knowledge base for forensic matches.
    """
    try:
        # Load the 'Frozen Brain' we will create in Step 4
        kb = joblib.load('src/vector_kb.joblib')
        
        # Convert user's text into a mathematical vector
        new_vector = EMBED_MODEL.encode([text_content])
        
        # Calculate how similar this is to our 75 trained examples
        similarities = cosine_similarity(new_vector, kb['embeddings'])[0]
        best_idx = similarities.argmax()
        score = similarities[best_idx]
        
        # Threshold: If it's more than 70% similar, we flag it as a finding
        if score > 0.70:
            return kb['labels'][best_idx], score
        return "Uncategorized", score
    except:
        # If vector_kb.joblib doesn't exist yet, we show this message
        return "Pending Local Training", 0.0

def analyze_forensic_workload(files_dict):
    """
    Finalized Day 3 Analyzer: Integrates Local ML flags + LLM Deep Analysis.
    """
    # 1. Self-Healing Client Initialization
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "❌ ERROR: GROQ_API_KEY not found in .env!"
    
    client = Groq(api_key=api_key)

    # 2. Evidence Preparation (Including Local ML Triage)
    combined_evidence = ""
    for filename, content in files_dict.items():
        # Here we use the local model to get a 'First Opinion'
        local_finding, confidence = get_vector_finding(content)
        
        combined_evidence += f"=== SOURCE FILE: {filename} ===\n"
        combined_evidence += f"[LOCAL ML RISK SCORE: {local_finding}]\n"
        combined_evidence += f"CONTENT: {content}\n\n"

    # 3. The Robust, Universal System Prompt
    system_prompt = (
        "You are a Senior Digital Forensic Investigator. Analyze the evidence "
        "and the 'LOCAL VECTOR MATCH' flags. Categorize findings ONLY using: "
        "Data Exfiltration, Evidence Tampering, Secrecy/Evasion, or Financial Anomaly.\n\n"
        
        "### FEW-SHOT EXAMPLES:\n"
        "1. Finding: | Data Exfiltration | 'Copied to SSD' | Moving data to external media. | Critical | chat.png |\n"
        "2. Finding: | Evidence Tampering | 'Wiped logs' | Use of secure deletion tools. | High | logs.txt |\n"
        "3. Finding: | Secrecy/Evasion | 'Meet at the spot' | Suspicious physical coordination. | High | cap.jpg |\n\n"
        
        "### OUTPUT FORMAT:\n"
        "Return a Markdown table with: | Category | Finding (Quote) | Significance | Risk |"
    )
       
    

    # 4. AI Execution
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this workload:\n{combined_evidence}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Analysis Failed: {e}"