from smolagents.tools import Tool

from services.flight_search.flight_search import FlightSearchService

class FlightSearchTool(Tool):
    name = "Flight Search"
    description = "Search for flights between two locations on a specific date."
    inputs = inputs = {
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
        'airline': {
            'type': 'string',
            'description': "The name of the airline to filter by.",
            'optional': True,
        },
        'max_price': {
            'type': 'number',
            'description': "The maximum price limit for flights.",
            'optional': True,
        },
        'max_stops': {
            'type': 'number',
            'description': "The maximum number of stops allowed for flights.",
            'optional': True,
        },
        'case_sensitive': {
            'type': 'boolean',
            'description': "Whether to perform case-sensitive matching for text fields.",
            'optional': True,
            'default': False,
        },
    }

    output_type = "string"

    def search_flights(self, origin, destination, departure_date, adults, children=0, infants=0):
        fss = FlightSearchService()
        flights = fss.search_with_filters()
        return flights
