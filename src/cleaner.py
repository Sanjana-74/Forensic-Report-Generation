import os
from groq import Groq
from dotenv import load_dotenv

# 1. Load the secrets from your .env file
load_dotenv()

# 2. Initialize the Groq client using your API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def clean_text(raw_text):
    """
    Uses Llama-3 to fix OCR errors and normalize text 
    while preserving every forensic detail.
    """
    
    # The 'System' prompt tells the AI how to behave
    system_prompt = (
        "You are a Forensic Data Assistant. Your job is to clean messy OCR text. "
        "Fix typos, normalize spacing, and correct obvious character errors (like '1' instead of 'l'). "
        "IMPORTANT: Do not summarize. Do not remove any facts, dates, or names. "
        "Return only the cleaned text."
    )

    # 3. Create the request to the AI
    # ... inside your clean_text function ...
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Clean this text: {raw_text}"}
        ],
      model="llama-3.3-70b-versatile",
        temperature=0.1,
    )

    # 4. Extract and return the cleaned text
    return chat_completion.choices[0].message.content