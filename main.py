# main.py
import json
#import ast
import time 
#from api_requests.discharge import discharge_on
from api_requests.get_request import get_request
from api_requests.post_request import post_request
def format_time(hour, minute):
    formatted_hour = f"0{hour}" if hour < 10 else str(hour)
    formatted_minute = f"0{minute}" if minute < 10 else str(minute)
    return f"{formatted_hour}:{formatted_minute}"

if __name__ == "__main__":
    
    #Get
    url_baseload = "http://127.0.0.1:5000/baseload"
    url_info = "http://127.0.0.1:5000/info"
    url_priceperhour = "http://127.0.0.1:5000/priceperhour"
    url_chargestate = "http://127.0.0.1:5000/charge"
    
    #Post
    url_charge_control = "http://127.0.0.1:5000/charge"
    #discharge_url = "http://127.0.0.1:5000/discharge"
    
    charging = False
    
    for _ in range(96):

        baseload_response = get_request(url_baseload)
        info_response = get_request(url_info) 
        price_per_hour_response = get_request(url_priceperhour)
        try:

            baseload_data = json.loads(baseload_response)
            info_data = json.loads(info_response)
            price_per_hour_data = json.loads(price_per_hour_response)
            

            if "sim_time_hour" in info_data and "sim_time_min" in info_data:
                time_hour = info_data["sim_time_hour"]
                time_minute = info_data["sim_time_min"]
                formatted_time = format_time(time_hour, time_minute)
                print(f"\n********** Time: {formatted_time} **********")

                price_per_hour_list = price_per_hour_data
                baseload_per_hour_list = baseload_data
                
                if price_per_hour_list:
                    found = False

                    for i, hourly_price in enumerate(price_per_hour_list):

                        if i == time_hour:
                            print(f"Price: {hourly_price} öre/kWh")
                            found = True
                            break

                    if not found:
                        print(f"Hour {time_hour} didnt found in price list.")
                else:
                    print("List of prices is empty.")
                
                if baseload_per_hour_list:
                    hourly_baseload = baseload_per_hour_list[time_hour]
                    print(f"Baseload: {hourly_baseload} kWh")
                else:
                    print("Baseload list is empty.")
                    
                
                print(f"Battery capacity: {info_data['battery_capacity_kWh']} kWh")
                print(f"Acutal baseload: {info_data['base_current_load']} kWh")
                    
            else:
                print("Key 'sim_time_hour' not found in JSON response.")
                
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
        
        chargestate = get_request(url_chargestate)
        print(f"Chargestate: {chargestate}%")
    
        sum_of_prices = sum(float(price) for price in price_per_hour_list)
        average_price = sum_of_prices/24
        
        sum_of_baseload = sum(float(baseload) for baseload in baseload_per_hour_list)
        average_usage = sum_of_baseload/24
        
        
        if hourly_price <= average_price and hourly_baseload <= 11 and hourly_baseload <= average_usage and float(chargestate) < 79.94:
            if not charging:
                charging_on = post_request(url_charge_control, charging=True)
                charging = True
                print("Charging turned ON")
        
        else:
            if charging:
                charging_off = post_request(url_charge_control, charging=False)
                charging = False
                print("Charging turned OFF")
                
        time.sleep(1)