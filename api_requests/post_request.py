# api_requests/post_request.py

import requests 

def post_request(url, charging=False):
    try: 
        payload = {"charging": "on" if charging else "off"}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Post function - charge: ")
        print(response.text)
        return response.text 
    
    except requests.exceptions.HTTPError as errH:
        print(f"HTTP-error: {errH}")
    except requests.exceptions.RequestException as err:
        print(f"Error with the request: {err}")
        return None