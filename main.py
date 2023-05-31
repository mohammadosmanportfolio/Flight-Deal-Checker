from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from FlightChecker import FlightChecker
from FlightDataManager import FlightDataManager
from NotificationSender import NotificationSender
import os

FROM_EMAIL = os.environ.get("MY_EMAIL") 
EMAIL_PASSWORD = os.environ.get("MY_EMAIL_PASSWORD") 
KIWI_API_KEY = os.environ.get("KIWI_API_KEY")

notification_sender = NotificationSender(from_email=FROM_EMAIL, to_email=FROM_EMAIL, 
                                         password=EMAIL_PASSWORD)

flight_data_manager = FlightDataManager(notification_sender=notification_sender)
flight_checker = FlightChecker(kiwi_api_endpoint="https://api.tequila.kiwi.com/v2/search",
                               kiwi_api_key=KIWI_API_KEY, 
                               data_manager=flight_data_manager)

today = datetime.now().strftime("%d/%m/%Y")
one_month = date.today() + relativedelta(months=+3)
one_month = one_month.strftime("%d/%m/%Y")

print("Which country or airport do you want to visit?")
destination = input("If entering an airport, please enter the airport's three letter IATA code. ")

flight_checker.get_lowest_flight_price_info(date_from=today, date_to=one_month, destination=destination)

