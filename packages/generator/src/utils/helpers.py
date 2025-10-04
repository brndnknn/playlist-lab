"""
Helper functions for making HTTP requests and parsing model output.

Includes JSON array extraction, key checking, and logged HTTP requests.
"""

import time
import random
import requests
from utils.logger_config import logger
from copy import deepcopy


SENSITIVE_KEYS = {
    "authorization",
    "proxy-authorization",
    "x-api-key",
    "api_key",
    "access_token",
    "refresh_token",
    "client_secret",
    "password",
    "token",
    "secret",
}


def _redact_value(value: str) -> str:
    try:
        s = str(value)
    except Exception:
        return "***REDACTED***"
    # Keep only last 4 chars for reference when long enough
    return ("***REDACTED***" if len(s) <= 8 else f"***REDACTED***…{s[-4:]}")


def _redact_mapping(mapping):
    try:
        data = deepcopy(mapping)
    except Exception:
        return "***REDACTED***"
    if isinstance(data, dict):
        redacted = {}
        for k, v in data.items():
            key_lower = str(k).lower()
            if key_lower in SENSITIVE_KEYS or any(w in key_lower for w in ("auth", "secret", "token", "password", "key")):
                redacted[k] = _redact_value(v)
            else:
                redacted[k] = v
        return redacted
    return data


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


def logged_request(method, url, retries: int = 4, backoff_base: float = 0.5, **kwargs):
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
            logger.debug(f"Query Params: {_redact_mapping(kwargs['params'])}")
        if 'json' in kwargs:
            logger.debug(f"JSON Body: {_redact_mapping(kwargs['json'])}")
        if 'headers' in kwargs:
            logger.debug(f"Headers: {_redact_mapping(kwargs['headers'])}")

        attempt = 0
        while True:
            try:
                response = requests.request(method, url, **kwargs)
                logger.info(f"Response Status: {response.status_code}")
                logger.debug(f"Response Headers: {_redact_mapping(response.headers)}")
                logger.debug(f"Response Body: {response.text}")

                # Retry on 429 and 5xx
                if response.status_code in {429, 500, 502, 503, 504} and attempt < retries:
                    delay = _retry_after_from_headers(response.headers)
                    if delay is None:
                        delay = backoff_base * (2 ** attempt) + random.uniform(0, 0.25)
                    logger.warning(f"Transient HTTP {response.status_code}; retrying in {delay:.2f}s")
                    time.sleep(delay)
                    attempt += 1
                    continue

                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                # Retry network errors/timeouts
                if attempt < retries:
                    delay = backoff_base * (2 ** attempt) + random.uniform(0, 0.25)
                    logger.warning(f"Request error '{e}'; retrying in {delay:.2f}s")
                    time.sleep(delay)
                    attempt += 1
                    continue
                raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

def _retry_after_from_headers(headers) -> float | None:
    """Best-effort extraction of server-suggested retry delay in seconds.

    Checks 'Retry-After' and common rate-limit reset headers.
    """
    try:
        h = {str(k).lower(): v for k, v in headers.items()}
        ra = h.get("retry-after")
        if ra is not None:
            try:
                return float(ra)
            except Exception:
                return None
        reset = h.get("x-ratelimit-reset") or h.get("x-ratelimit-reset-requests") or h.get("x-ratelimit-reset-tokens")
        if reset is not None:
            try:
                val = float(reset)
                if val > 1e6:
                    return max(0.0, val - time.time())
                return max(0.0, val)
            except Exception:
                return None
    except Exception:
        return None
    return None
    

