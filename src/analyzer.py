import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_forensic_workload(files_dict):
    """
    Finalized Day 3 Analyzer: Handles multiple files, 
    identifies correlations, and uses robust few-shot examples.
    """
    # 1. Self-Healing Client Initialization
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "❌ ERROR: GROQ_API_KEY not found in .env!"
    
    client = Groq(api_key=api_key)

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
        
        "### OUTPUT FORMAT:\n"
        "Return your findings in a Markdown TABLE, followed by a 'CROSS-FILE CORRELATIONS' section."
    )

    # 4. AI Execution
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this evidence set:\n{combined_evidence}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Analysis Failed: {e}"