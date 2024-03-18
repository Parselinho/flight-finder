class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(
        self,
        from_city_code,
        from_city_name,
        to_city_code,
        to_city_name,
        price,
        nights_in_dest,
        airline,
        bag_price,
        availability,
        fly_duration,
        flight_time,
        back_flight_time,
        deal_url,
    ) -> None:
        self.from_city_code = from_city_code
        self.to_city_code = to_city_code
        self.from_city_name = from_city_name
        self.to_city_name = to_city_name
        self.price = price
        self.nights_in_dest = nights_in_dest
        self.airline = airline
        self.bag_price = bag_price
        self.availability = availability
        self.fly_duration = fly_duration
        self.flight_time = flight_time
        self.back_flight_time = back_flight_time
        self.deal_url = deal_url
