# utils.py
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_text_from_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
