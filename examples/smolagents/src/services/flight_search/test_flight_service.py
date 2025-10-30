from src.services.flight_search.flight_search import FlightSearchService

def test_flight_service_search():
    fss = FlightSearchService()
    results = fss.find_by_route("Madrid", "Barcelona")

    assert isinstance(results, list)
    assert len(results) > 0
