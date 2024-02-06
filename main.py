# main.py
import json
import ast
import time 
from api_requests.discharge import discharge_on
from api_requests.get_request import get_request
from api_requests.post_request import post_request
def format_time(hour):
    if hour < 10:
        return f"0{hour}:00"
    else:
        return f"{hour}:00"

if __name__ == "__main__":
    
    #Get
    url_baseload = "http://127.0.0.1:5000/baseload"
    url_info = "http://127.0.0.1:5000/info"
    url_priceperhour = "http://127.0.0.1:5000/priceperhour"
    url_chargestate = "http://127.0.0.1:5000/charge"
    
    #Post
    url_charge_control = "http://127.0.0.1:5000/charge"
    discharge_url = "http://127.0.0.1:5000/discharge"
    
    charging = False
    
    for _ in range(24):
        baseload_response = get_request(url_baseload)
        info_response = get_request(url_info) 

        try:
            # Försök konvertera serverresponsen till JSON
            baseload_data = json.loads(baseload_response)
            info_data = json.loads(info_response)
            
            # Om "sim_time_hour" finns i JSON, hämta värdet
            if "sim_time_hour" in info_data:
                time_hour = info_data["sim_time_hour"]
                formatted_time = format_time(time_hour)
                print(f"\n********** Time: {formatted_time} **********")

                # Kontrollera att det finns en lista med priser
                price_per_hour_list = ast.literal_eval(get_request(url_priceperhour))
                baseload_per_hour = baseload_data
                
                if price_per_hour_list:
                    found = False
                    # Iterera över varje timme i listan
                    for i, hourly_price in enumerate(price_per_hour_list):
                        # Jämför med "sim_time_hour"
                        if i == time_hour:
                            print(f"Price: {hourly_price} kr/kWh")
                            found = True
                            break

                    # Om timmen inte hittades i listan
                    if not found:
                        print(f"Hour {time_hour} didnt found in price list.")
                else:
                    print("List of prices is empty.")
                
                if baseload_per_hour:
                    hourly_baseload = baseload_per_hour[time_hour]
                    print(f"Baseload: {hourly_baseload} kWh")
                else:
                    print("Baseload list is empty.")
                    
                # Utskrift av batterikapacitet och aktuell basbelastning
                print(f"Battery capacity: {info_data['battery_capacity_kWh']} kWh")
                print(f"Acutal baseload: {info_data['base_current_load']} kWh")
                    
            else:
                print("Key 'sim_time_hour' not found in JSON response.")
                
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
        
        chargestate = get_request(url_chargestate)
        print(f"Chargestate: {chargestate} %")
    
        sum_of_prices = sum(float(price) for price in price_per_hour_list)
        average_price = sum_of_prices/24
        
        sum_of_baseload = sum(float(baseload) for baseload in baseload_per_hour)
        average_usage = sum_of_baseload/24
        
        if time_hour == 16: 
            discharge_on(discharge_url)
        
        # Ladda bara om timpriset är mindre än det genomsnittliga priset och laddningsstaten är mindre än 79.94%
        if hourly_price <= average_price and float(chargestate) < 79.94:
            if not charging:
                charging_on = post_request(url_charge_control, charging=True)
                charging = True
                print("Charging turned ON")
        
        else:
            if charging:
                charging_off = post_request(url_charge_control, charging=False)
                charging = False
                print("Charging turned OFF")
                
        time.sleep(4)