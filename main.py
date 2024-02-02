# main.py
import json
import ast
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
    
    baseload = get_request(url_baseload) #, topic="baseload"
    get_request(url_info) #, topic="household info"
    price_per_hour = get_request(url_priceperhour) #, topic="price per hour"
    
    chargestate = get_request(url_chargestate) #, topic="charge state of the car"
    
    print(chargestate) 
   
    price_per_hour_list = ast.literal_eval(price_per_hour)
    sum_of_prices = sum(float(price) for price in price_per_hour_list)
    print("sum of prices", sum_of_prices)
    average_price = sum_of_prices/24
    
    print("average price",average_price)
    
    if float(chargestate) < 79.94: 
        charging_on = post_request(url_charge_control, charging=True)
        print(charging_on)
    
    else:
        charging_off = post_request(url_charge_control, charging=False)
        print(charging_off)