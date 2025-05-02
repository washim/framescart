import re

def extract_number_from_parentheses(text):
    match = re.search(r'\(+([-+]?\d+(\.\d+)?) Rs\)', text)
    
    if match:
        return int(match.group(1))
    
    return 0