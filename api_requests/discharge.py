import requests

def discharge_on(url):
    try:
        payload = {"discharging": "on"}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Discharge function - discharging on:")
        print(response.text)
        return response.text

    except requests.exceptions.HTTPError as errH:
        print(f"HTTP-error: {errH}")
    except requests.exceptions.RequestException as err:
        print(f"Error with the request: {err}")
        return None