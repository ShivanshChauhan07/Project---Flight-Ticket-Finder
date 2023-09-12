import requests
from tkinter import messagebox
sheety_url = "https://api.sheety.co/8b809bac16ff2e13c6afde194de76585/flightDeals/prices"


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=sheety_url)
        data = response.json()
        self.destination_data = data["prices"]

        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price":{
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{sheety_url}/{city['id']}",json=new_data)
            print(response.text)
        messagebox.showinfo("Request Status", "City's IataCodes append in the Google Sheet Successfully !")

    def post_destination_data(self,destinationCity,lowestPrice):
        new_row = {
            "price":{
            "city": destinationCity,
            "lowestPrice":lowestPrice
        }
        }
        try:
            response = requests.post(url=sheety_url,json=new_row)
            messagebox.showinfo("Request Status","City's append Successfully in Google Sheet !")
        except:
            messagebox.showinfo("Error", "Something Went Wrong !")