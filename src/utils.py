import hashlib
from datetime import datetime
import uuid

def get_file_hash(file_bytes):
    """Generates a SHA-256 digital fingerprint of the file."""
    return hashlib.sha256(file_bytes).hexdigest()

def get_timestamp():
    """Returns the current time in a professional format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_case_id():
    """Creates a unique ID for the forensic case."""
    return f"CASE-{str(uuid.uuid4())[:8].upper()}"