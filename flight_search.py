import requests
from flight_data import FlightData
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
FLIGHTSEARCHAPI = "H6E7uQQaO9MKAPiRFg0QqMgH2X0Huexs"

class FlightSearch:
    def get_destination_code(self,city_name):
        header = {
            "apikey": FLIGHTSEARCHAPI
        }
        query ={
            "term":city_name,
            "local_types": "city",
            "limit": 1,
            "active_only": True
        }
        response = requests.get(url=f"{TEQUILA_ENDPOINT}/locations/query",headers=header,params=query)
        data = response.json()["locations"]
        return data[0]["code"]

    def check_flight(self,des_city_code,from_time,to_time):
        header = {
            "apikey":FLIGHTSEARCHAPI
        }
        query = {
            "fly_from": "DEL",
            "fly_to": des_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
            "limit": 1
        }

        response = requests.get(url=f"{TEQUILA_ENDPOINT}/v2/search",headers=header,params=query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print("No flights Found")
            return None

        flight_data = FlightData(price=data["price"],
                                 origin_city=data["cityFrom"],
                                 origin_airport=data["flyFrom"],
                                 destination_city=data["cityTo"],
                                 destination_airport=data["flyTo"],
                                 out_date=data["route"][0]["local_departure"].split("T")[0],
                                 return_date=data["route"][1]["local_departure"].split("T")[0])
        print(f"{flight_data.destination_city}: $ {flight_data.price}")
        return flight_data
