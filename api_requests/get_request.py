# api_requests/get_request.py

import requests

def get_request(url): #, topic=None
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("GET function: ")  #{topic}
        print(response.text)
        print("-----------------------------------------------------------------------------------------------------------------------")
        return response.text  # Returnera svaret
        
    except requests.exceptions.HTTPError as errH:
        print(f"Http-error: {errH}")
    except requests.exceptions.RequestException as err:
        print(f"Error with the request: {err}")
        return None