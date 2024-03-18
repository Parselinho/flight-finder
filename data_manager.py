import os

# from data_demo import data_demo
from http_request import HttpRequester

from pprint import pprint


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self, http_method: HttpRequester) -> None:
        self.base_url = f"{os.environ.get('SHEETS_ENDPOINT')}/flightDeals/prices"
        self.header = os.environ.get("SHEETS_AUTH")
        self.http_method = http_method

    def get_data_from_sheets(self):
        # data = data_demo
        data = self.http_method.get(url=self.base_url)
        return data

    def update_data_in_sheets(self, city):
        new_data = {"price": {"iataCode": city["iataCode"]}}
        r = self.http_method.put(
            url=f"{self.base_url}/{city['id']}",
            json=new_data,
            headers={"Authorization": f"Bearer {self.header}"},
        )
        return r

    def update_lowest_price_in_sheets(self, city_id, new_lowest_price):
        update_data = {"price": {"lowestPrice": new_lowest_price}}
        response = self.http_method.put(
            url=f"{self.base_url}/{city_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {self.header}"},
        )
        return response
