import os
from pprint import pprint
from http_request import HttpRequester
from datetime import datetime, timedelta
from flight_data import FlightData


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self, http_method: HttpRequester) -> None:
        self.api_key = {"apikey": os.environ.get("FLIGHT_SEARCH_API_KEY")}
        self.base_url = "https://api.tequila.kiwi.com"
        self.timeout = 5
        self.http_method = http_method
        self.half_year_date = datetime.now() + timedelta(weeks=26)

    def get_iata_codes(self, city):
        url = f"{self.base_url}/locations/query"
        params = {"term": f"{city}", "location_types": "city"}
        r = self.http_method.get(url=url, params=params, headers=self.api_key)
        return r["locations"][0]["code"]

    def search_for_flighs(
        self,
        from_city_code="TLV",
        to_city_code="PAR",
        date_from=None,
        date_to=None,
        nights_in_dst_from=7,
        nights_in_dst_to=28,
        adults=1,
        children=0,
        infants=0,
        selected_cabins="M",
        curr="ILS",
        max_stopovers=0,
    ):
        # fixing the date_from and date_to params, to default values if the user is not using them
        if date_from is None:
            today_date = datetime.now() + timedelta(days=1)
            date_from = self.format_date(today_date)
        if date_to is None:
            half_year_date = datetime.now() + timedelta(weeks=36)
            date_to = self.format_date(half_year_date)
        url = f"{self.base_url}/search"
        params = {
            "fly_from": f"city:{from_city_code}",
            "fly_to": f"city:{to_city_code}",
            "date_from": f"{date_from}",
            "date_to": f"{date_to}",
            "nights_in_dst_from": nights_in_dst_from,
            "nights_in_dst_to": nights_in_dst_to,
            "one_for_city": 1,
            "adults": adults,
            "children": children,
            "infants": infants,
            "selected_cabins": f"{selected_cabins}",
            "curr": curr,
            "max_stopovers": max_stopovers,
        }

        r = self.http_method.get(url=url, params=params, headers=self.api_key)
        try:
            response_data = r["data"][0]
        except IndexError:
            print(f"there is no flight found this time for{to_city_code}")
            return None

        flight_data = FlightData(
            from_city_code=response_data["cityCodeFrom"],
            to_city_code=response_data["cityCodeTo"],
            from_city_name=response_data["cityFrom"],
            to_city_name=response_data["cityTo"],
            price=response_data["price"],
            nights_in_dest=response_data["nightsInDest"],
            airline=response_data["route"][0]["airline"],
            bag_price=response_data["bags_price"]["1"],
            availability=response_data["availability"]["seats"],
            fly_duration=response_data["fly_duration"],
            flight_time=self.format_utc(response_data["route"][0]["aTimeUTC"]),
            back_flight_time=self.format_utc(response_data["route"][1]["aTimeUTC"]),
            deal_url=response_data["deep_link"],
        )
        pprint(f"{flight_data.to_city_name}: {flight_data.price} Shekels")
        return flight_data

    def format_date(self, _date):
        return _date.strftime("%d/%m/%Y")

    def format_utc(self, time):
        return datetime.fromtimestamp(time).strftime("%Y-%m-%d %H:%M")
