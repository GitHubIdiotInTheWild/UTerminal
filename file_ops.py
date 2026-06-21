# file_ops.py
import os
from utils import format_size

def list_directory():
    """Returns a formatted string of everything in the current directory."""
    try:
        items = os.listdir('.')
        if not items:
            return "Directory is empty.\n"
        
        output = []
        output.append(f"{'NAME':<30} | {'TYPE':<10} | {'SIZE':<10}")
        output.append("-" * 60)
        
        for item in items:
            if os.path.isdir(item):
                output.append(f"{item:<30} | {'DIR':<10} | {'--':<10}")
            else:
                size = os.path.getsize(item)
                output.append(f"{item:<30} | {'FILE':<10} | {format_size(size):<10}")
                
        return "\n".join(output) + "\n"
    except Exception as e:
        return f"Error listing directory: {str(e)}\n"

def make_file(filename):
    """Creates an empty file."""
    try:
        with open(filename, 'a'):
            os.utime(filename, None)
        return f"Successfully created file: {filename}\n"
    except Exception as e:
        return f"Error creating file: {str(e)}\n"