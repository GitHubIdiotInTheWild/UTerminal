# file_viewer.py
import os

def read_file_content(filename):
    """Reads and returns text from a file safely."""
    if not os.path.exists(filename):
        return f"Error: File '{filename}' does not exist.\n"
    if os.path.isdir(filename):
        return f"Error: '{filename}' is a directory, cannot read as text.\n"
        
    try:
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return f"\n--- CONTENTS OF {filename} ---\n{content}\n---------------------------\n"
    except Exception as e:
        return f"Error reading file: {str(e)}\n"