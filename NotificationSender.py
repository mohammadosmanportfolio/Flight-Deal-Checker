import smtplib, os

SMTP_HOST = os.environ.get("SMTP_HOST")

class NotificationSender:
    def __init__(self, from_email: str, to_email: str, password):
        self.from_email = from_email
        self.to_email = to_email
        self.password = password

    #notification is now sent through email
    def send_notification(self, data: dict):
        with smtplib.SMTP(host=SMTP_HOST) as connection:
            connection.starttls()
            connection.login(user=self.from_email, password=self.password)
            city = data['city']
            iata = data['iataCode']
            price = data['lowestPrice']
            message = f"""\
Subject: Fly to {city}!

A flight to {city} through {iata} airport is now $CAD {price}."""
            connection.sendmail(from_addr=self.from_email, to_addrs=self.to_email, msg=message)