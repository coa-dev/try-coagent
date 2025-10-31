from smolagents.tools import Tool

from services.flight_search.flight_search import FlightSearchService

class FlightSearchTool(Tool):
    name = "flight_search"
    description = "Search for flights between two locations"
    inputs = {
        'source': {
            'type': 'string',
            'description': "The name or code of the source airport or city.",
            'optional': True,
        },
        'destination': {
            'type': 'string',
            'description': "The name or code of the destination airport or city.",
            'optional': True,
        },
    }
    output_type = 'string'

    def __init__(self, **kwargs):
        super().__init__()

    def forward(self, source: str, destination: str) -> str:
        fss = FlightSearchService()
        flights = fss.find_by_route(source, destination)

        if len(flights) == 0:
            flights = [
                {
                    "Airline": "Mock Airline",
                    "FlightNumber": "MA123",
                    "Source": source,
                    "Destination": destination,
                    "DepartureTime": "2024-07-01T10:00:00",
                    "ArrivalTime": "2024-07-01T12:00:00",
                    "Price": 199.99
                },
                {
                    "Airline": "Sample Air",
                    "FlightNumber": "SA456",
                    "Source": source,
                    "Destination": destination,
                    "DepartureTime": "2024-07-01T15:00:00",
                    "ArrivalTime": "2024-07-01T17:00:00",
                    "Price": 249.99
                },
                {
                    "Airline": "Test Flights",
                    "FlightNumber": "TF789",
                    "Source": source,
                    "Destination": destination,
                    "DepartureTime": "2024-07-01T18:00:00",
                    "ArrivalTime": "2024-07-01T20:00:00",
                    "Price": 179.99
                },
                {
                    "Airline": "Demo Airways",
                    "FlightNumber": "DA101",
                    "Source": source,
                    "Destination": destination,
                    "DepartureTime": "2024-07-01T20:00:00",
                    "ArrivalTime": "2024-07-01T22:00:00",
                    "Price": 229.99
                }
            ]

        return flights
