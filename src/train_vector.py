import pandas as pd
from sentence_transformers import SentenceTransformer
import joblib
import os

def train_knowledge_base():
    """
    The Brain Builder: Converts 75 forensic patterns into 
    384-dimensional vectors for semantic matching.
    """
    csv_path = 'data/training_data.csv'
    output_path = 'src/vector_kb.joblib'

    # 1. Safety Check
    if not os.path.exists(csv_path):
        print(f"❌ CRITICAL ERROR: {csv_path} not found!")
        return

    # 2. Load the 75-row Dataset
    print("📂 Loading 75-row forensic dataset...")
    df = pd.read_csv(csv_path)

    # 3. Load the Transformer Model
    print("⏳ Loading AI Model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 4. Vectorization (The actual 'Training')
    print(f"🧠 Encoding {len(df)} forensic patterns. This may take a moment...")
    embeddings = model.encode(df['text'].tolist())

    # 5. Save the Knowledge Base
    kb_data = {
        "embeddings": embeddings,
        "labels": df['category'].tolist(),
        "model_name": 'all-MiniLM-L6-v2'
    }
    
    joblib.dump(kb_data, output_path)
    print(f"✅ SUCCESS: {output_path} has been created!")
    print("🚀 Your local intelligence layer is now ACTIVE.")

if __name__ == "__main__":
    train_knowledge_base()