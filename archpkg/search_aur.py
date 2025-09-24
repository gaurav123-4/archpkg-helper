import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import json

def search_aur(query):
    if not query or not query.strip():
        raise ValueError("Empty search query provided")
        
    url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={query.strip()}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            raise RequestException(f"Invalid response from AUR: {str(e)}")
            
        if not isinstance(data, dict):
            raise RequestException("Unexpected response format from AUR")
            
        results = data.get("results", [])
        if not isinstance(results, list):
            raise RequestException("Invalid results format from AUR")
            
        return [(pkg['Name'], pkg.get('Description', 'No description'), 'AUR') for pkg in results if isinstance(pkg, dict) and 'Name' in pkg]
        
    except ConnectionError:
        raise ConnectionError("Cannot connect to AUR servers. Check your internet connection.")
    except Timeout:
        raise Timeout("AUR search request timed out. Try again later.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise RequestException("AUR rate limit exceeded. Please wait before searching again.")
        elif e.response.status_code >= 500:
            raise RequestException("AUR servers are experiencing issues. Try again later.")
        else:
            raise RequestException(f"AUR request failed with status {e.response.status_code}")
    except Exception as e:
        raise RequestException(f"AUR search failed: {str(e)}")