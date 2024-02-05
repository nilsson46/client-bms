# main.py
import json
import ast
import time 
from api_requests.get_request import get_request
from api_requests.post_request import post_request
if __name__ == "__main__":
    
    #Get
    url_baseload = "http://127.0.0.1:5000/baseload"
    url_info = "http://127.0.0.1:5000/info"
    url_priceperhour = "http://127.0.0.1:5000/priceperhour"
    url_chargestate = "http://127.0.0.1:5000/charge"
    
    #Post
    url_charge_control = "http://127.0.0.1:5000/charge"
    
    for _ in range(24):
        baseload = get_request(url_baseload) #, topic="baseload"
        info_response = get_request(url_info) #, topic="household info"
        
        try:
            # Försök konvertera serverresponsen till JSON
            json_data = json.loads(info_response)
            
            # Om "sim_time_hour" finns i JSON, hämta värdet
            if "sim_time_hour" in json_data:
                time_hour = json_data["sim_time_hour"]
                print("Sim Time Hour:", time_hour)

                # Kontrollera att det finns en lista med priser
                price_per_hour_list = ast.literal_eval(get_request(url_priceperhour))
                if price_per_hour_list:
                    found = False
                    # Iterera över varje timme i listan
                    for i, hourly_price in enumerate(price_per_hour_list):
                        # Jämför med "sim_time_hour"
                        if i == time_hour:
                            print(f"Priset vid timme {time_hour}: {hourly_price}")
                            found = True
                            break

                    # Om timmen inte hittades i listan
                    if not found:
                        print(f"Timme {time_hour} hittades inte i listan.")
                else:
                    print("Lista med priser är tom.")
            else:
                print("Key 'sim_time_hour' not found in JSON response.")

        except json.JSONDecodeError:
            print("Error decoding JSON response.")
        
        chargestate = get_request(url_chargestate)
        
        print(chargestate) 
    
        sum_of_prices = sum(float(price) for price in price_per_hour_list)
        average_price = sum_of_prices/24
        
        
        if hourly_price <= average_price and float(chargestate) < 79.94:
            charging_on = post_request(url_charge_control, charging=True)

        
        else:
            charging_off = post_request(url_charge_control, charging=False)
        time.sleep(4)
