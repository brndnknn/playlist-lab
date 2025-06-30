"""
Helper functions for making HTTP requests and parsing model output.

Includes JSON array extraction, key checking, and logged HTTP requests.
"""

import requests
from utils.logger_config import logger


def extract_array(text):
    """
    Extracts and returns the first JSON array substring from text. 

    Args:
        text (str): String potentially containing a JSON array.
    
    Returns:
        str: The extracted JSON array or original text if not found.
    """
    start_index = text.find('[')
    end_index = text.find(']')

    if start_index == -1 or end_index == -1 or end_index < start_index:
        return text
    
    return text[start_index:end_index + 1]

def has_keys(obj, key1, key2):
    """
    Checks if a dict contains both keys.

    Args:
        obj (dict): The dictionary to check.
        key1 (str): First key to check.
        key2 (str): Second key to check.

    Returns:
        bool: True if both keys are present.
    """
    if not isinstance(obj, dict):
        return False 
    return key1 in obj and key2 in obj


def logged_request(method, url, **kwargs):
    """
    Makes an HTTP request and logs detailed request/response info.

    Args:
        method (str): HTTP method 'GET', 'POST', etc.
        url (str): Full URL to request.
        **kwargs: Another keyword arguments for requests.request.

    Returns:
        requests.Response: The HTTP response object.
    
    Raises:
        requests.RequestException: If the request fails.
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