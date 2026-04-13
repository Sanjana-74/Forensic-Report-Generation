from src.analyzer import analyze_forensic_workload

# We simulate a "Smoking Gun" scenario
mock_evidence = {
    "secret_chat.png": "Alice: I've moved the blueprint to the folder named 'Project-X'.",
    "file_logs.txt": "User 'Alice' created a new directory: /hidden/Project-X/ at 14:30."
}

print("🔎 Running Cross-File Correlation Test...")
result = analyze_forensic_workload(mock_evidence)

print("\n" + "="*50)
print("AI INVESTIGATION RESULTS")
print("="*50)
print(result)