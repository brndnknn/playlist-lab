import json

def extract_array(text):
    start_index = text.find('[')
    end_index = text.find(']')

    if start_index == -1 or end_index == -1 or end_index < start_index:
        return text
    
    return text[start_index:end_index + 1]

def has_keys(obj, key1, key2):
    if not isinstance(obj, dict):
        return False 
    return key1 in obj and key2 in obj