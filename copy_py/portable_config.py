# portable_config.py
import os
import sys
import pytesseract
import subprocess

def setup_portable_environment():
    
    current_dir = os.path.dirname(os.path.abspath(__file__)))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    try:
        result = subprocess.run(['where', 'tesseract'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            tesseract_path = result.stdout.split('\n')[0].strip()
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
    except:
        pass

setup_portable_environment()