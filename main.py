# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from http_request import HttpRequester
from pprint import pprint

http_method = HttpRequester()
data = DataManager(http_method)

send_sms = NotificationManager()


sheet_data = data.get_data_from_sheets()["prices"]

flight_search = FlightSearch(http_method)

for city in sheet_data:
    if city["iataCode"] == "":
        city["iataCode"] = flight_search.get_iata_codes(city["city"])
        # data.data = sheet_data ---> i dont understand why angela used it, but i dont find it necessary
        data.update_data_in_sheets(city)

for city in sheet_data:
    flight_data = flight_search.search_for_flighs(to_city_code=city["iataCode"])
    if flight_data.price < city["lowestPrice"] or city["lowestPrice"] == "":
        send_sms.send_message(
            msg_value=f"Low Price Alert! I found for you the lowest price for flight from {flight_data.from_city_name} to {flight_data.to_city_name} only in {flight_data.price} Shekels, with {flight_data.airline}. bag only for {flight_data.bag_price}, for {flight_data.nights_in_dest} Nights, departure time: {flight_data.flight_time}, back in {flight_data.back_flight_time}. you have {flight_data.availability} places left. you can find it in this link: {flight_data.deal_url}"
        )
        city["lowestPrice"] = data.update_lowest_price_in_sheets(
            city_id=city["id"], new_lowest_price=flight_data.price
        )
