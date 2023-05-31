import requests, pycountry
from FlightDataManager import FlightDataManager
class FlightChecker:

    #I will manually enter the departure location as "LAX" in Los Angeles, for the sake
    #of this project
    def __init__(self, kiwi_api_endpoint, kiwi_api_key, data_manager: FlightDataManager):
        self.data_manager = data_manager
        self.fly_from = "LAX"
        self.kiwi_api_endpoint = kiwi_api_endpoint
        self.kiwi_api_key = kiwi_api_key

    #used to get the destination. The if statement checks if the user entered a three-letter
    #airport code. If so, return this. If not, that means they must have entered a country's name,
    #so we will use this as the class's self.fly_to attribute
    def get_destination_code(self, destination):
        if len(destination) != 3:
            return pycountry.countries.get(name=destination).alpha_2.upper()
        else:
            return destination.upper()

    #this method gets the information for the current lowest price of the user's destination
    #we will then use the data manager to do all necessary work with this information
    def get_lowest_flight_price_info(self, destination, date_from, date_to):
        dest = self.get_destination_code(destination=destination)
        kiwi_header = {
            "apikey": self.kiwi_api_key
        }

        kiwi_body = {
            "fly_from": self.fly_from,
            "fly_to": dest,
            "date_from": date_from,
            "date_to": date_to,
            "only_weekends": True,
            "curr": "CAD",
            "limit": 500
        }

        response = requests.get(url=self.kiwi_api_endpoint, params=kiwi_body, headers=kiwi_header)
        response.raise_for_status()
        data = response.json()['data'][0]
        return_this_object = {
            "Destination City": data['cityTo'],
            "Destination Airport": data['flyTo'],
            "Price": data['price']
        }
        self.data_manager.add_flight_data(new_data=return_this_object)
        
    
