import requests, os
from NotificationSender import NotificationSender

SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
SHEETY_FLIGHT_BEARER_TOKEN = os.environ.get("SHEETY_FLIGHT_BEARER_TOKEN")
sheety_header = {
            "Authorization": f"Bearer {SHEETY_FLIGHT_BEARER_TOKEN}"
        }

class FlightDataManager:
    def __init__(self, notification_sender: NotificationSender):
        self.flight_data: list
        self.flight_data = self.get_flight_data()
        self.notification_sender = notification_sender

    #Method used to initialize the class's self.flight_data attribute
    def get_flight_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, headers=sheety_header)
        response.raise_for_status()
        return response.json()['prices'] 
    
    #entry is in the spreadsheet and program found a lower price. Update the price in the spreadsheet
    def update_price(self, new_data: dict):
        dest_city = new_data['city']
        dest_iata = new_data['iataCode']
        #getting the id of the destination's entry in the spreadsheet. Will need to append it to new
        #api endpoint
        for entry in self.flight_data:
            if dest_city == entry['city'] or dest_iata == entry['iataCode']:
                dest_id = entry['id']
                break
        new_sheety_endpoint = SHEETY_ENDPOINT + "/" + str(dest_id)
        sheety_body = {
            "price": {
                "city": dest_city,
                "iataCode": dest_iata,
                "lowestPrice": new_data['lowestPrice']
            }
        }
        requests.put(url=new_sheety_endpoint, headers=sheety_header,
                                json=sheety_body)
        self.notification_sender.send_notification(data=sheety_body['price'])

    def add_flight_data(self, new_data: dict):
        dest_city = new_data['Destination City']
        dest_iata = new_data['Destination Airport']
        new_price = new_data['Price']
        current_lowest_price = self.get_cheapest_flight_for_dest(dest_city=dest_city, 
                                                                 dest_iata=dest_iata)
        if current_lowest_price == None:
            #destination isn't in the spreadsheet. Enter it as a new entry in spreadsheet and
            #append it to self.flight_data attribute
            sheety_body = {
                "price": {
                    "city": dest_city,
                    "iataCode": dest_iata,
                    'lowestPrice': str(new_price)
                }
            }
            response = requests.post(url=SHEETY_ENDPOINT, json=sheety_body, headers=sheety_header)
            append_this_entry = {
                "city": dest_city,
                "iataCode": dest_iata,
                "lowestPrice": str(new_price),
                "id": response.json()['price']['id']
            }
            self.flight_data.append(append_this_entry)

        elif float(new_price) < float(current_lowest_price):
            update_with_this_info = {
                "city": dest_city,
                "iataCode": dest_iata,
                "lowestPrice": str(new_price),
            }
            self.update_price(new_data=update_with_this_info)

    def get_cheapest_flight_for_dest(self, dest_city: str, dest_iata: str):
        for entry in self.flight_data:
            if entry['city'] == dest_city or entry['iataCode'] == dest_iata:
                return entry['lowestPrice']
            else:
                return None

