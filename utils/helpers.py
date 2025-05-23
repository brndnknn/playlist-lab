import requests
from utils.logger_config import logger


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

def is_valid_json_playlist(output):
    """Returns True if the output is valid JSON representing a playlist:
    a list of at least 5 objects with keys 'title' and 'artist'."""
    try:
        parsed = json.loads(output)
        if isinstance(parsed, list) and len(parsed) >= 5:
            return all(isinstance(item, dict) and "title" in item and "artist" in item for item in parsed)
        return False
    except Exception:
        return False


def logged_request(method, url, **kwargs):
    """
    Makes an HTTP request and logs detailed request/response info.

    Args:
        method (str): 'GET', 'POST', etc.
        url (str): Full URL to request.
        **kwargs: Another keyword arguments for requests.request.

    Returns:
        requsets.Response: The HTTP response object.
    """

    try:
        logger.info(f"HTTP {method.upper()} {url}")
        if 'params' in kwargs:
            logger.debug(f"Query Params: {kwargs['params']}")
        if 'json' in kwargs:
            logger.debug(f"JSON Body: {kwargs['json']}")
        if 'headers' in kwargs:
            logger.debug(f"Headers: {kwargs['headers']}")

        response = requests.request(method, url, **kwargs)

        logger.info(f"Response Status: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Body: {response.text}")

        response.raise_for_status()
        return response
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise