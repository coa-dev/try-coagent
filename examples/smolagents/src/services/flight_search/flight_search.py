import pandas as pd

from typing import Optional, List, Dict

class FlightSearchService:
    """
    A class to search airline records based on source and destination.
    """

    def __init__(self):
        self.csv_file_path = "../../../data/flight_dataset.csv"
        self.data = None
        self._load_data()

    def _load_data(self):
        """Load data from CSV file."""
        try:
            self.data = pd.read_csv(self.csv_file_path)
            print(f"Loaded {len(self.data)} records from {self.csv_file_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")

    def find_by_route(self, source: str, destination: str,
                      case_sensitive: bool = False) -> pd.DataFrame:
        """
        Find records by source and destination.

        Args:
            source (str): Source city
            destination (str): Destination city
            case_sensitive (bool): Whether to perform case-sensitive search

        Returns:
            pd.DataFrame: Filtered records matching the criteria
        """
        if self.data is None:
            raise ValueError("No data loaded")

        if not case_sensitive:
            source_mask = self.data['Source'].str.lower() == source.lower()
            dest_mask = self.data['Destination'].str.lower() == destination.lower()
        else:
            source_mask = self.data['Source'] == source
            dest_mask = self.data['Destination'] == destination

        result = self.data[source_mask & dest_mask]
        return result

    def find_by_source(self, source: str, case_sensitive: bool = False) -> pd.DataFrame:
        """
        Find all records from a specific source city.

        Args:
            source (str): Source city
            case_sensitive (bool): Whether to perform case-sensitive search

        Returns:
            pd.DataFrame: All records from the source city
        """
        if self.data is None:
            raise ValueError("No data loaded")

        if not case_sensitive:
            mask = self.data['Source'].str.lower() == source.lower()
        else:
            mask = self.data['Source'] == source

        return self.data[mask]

    def find_by_destination(self, destination: str, case_sensitive: bool = False) -> pd.DataFrame:
        """
        Find all records to a specific destination city.

        Args:
            destination (str): Destination city
            case_sensitive (bool): Whether to perform case-sensitive search

        Returns:
            pd.DataFrame: All records to the destination city
        """
        if self.data is None:
            raise ValueError("No data loaded")

        if not case_sensitive:
            mask = self.data['Destination'].str.lower() == destination.lower()
        else:
            mask = self.data['Destination'] == destination

        return self.data[mask]

    def get_cheapest_route(self, source: str, destination: str,
                          case_sensitive: bool = False) -> Optional[pd.Series]:
        """
        Get the cheapest flight for a specific route.

        Args:
            source (str): Source city
            destination (str): Destination city
            case_sensitive (bool): Whether to perform case-sensitive search

        Returns:
            pd.Series or None: Record of the cheapest flight, None if no flights found
        """
        routes = self.find_by_route(source, destination, case_sensitive)

        if routes.empty:
            return None

        cheapest_idx = routes['Price'].idxmin()
        return routes.loc[cheapest_idx]

    def get_all_routes(self) -> List[tuple]:
        """
        Get all unique source-destination pairs.

        Returns:
            List[tuple]: List of (source, destination) tuples
        """
        if self.data is None:
            raise ValueError("No data loaded")

        routes = self.data[['Source', 'Destination']].drop_duplicates()
        return [(row['Source'], row['Destination']) for _, row in routes.iterrows()]

    def get_airlines_for_route(self, source: str, destination: str,
                              case_sensitive: bool = False) -> List[str]:
        """
        Get all airlines serving a specific route.

        Args:
            source (str): Source city
            destination (str): Destination city
            case_sensitive (bool): Whether to perform case-sensitive search

        Returns:
            List[str]: List of unique airlines serving the route
        """
        routes = self.find_by_route(source, destination, case_sensitive)

        if routes.empty:
            return []

        return routes['Airline'].unique().tolist()

    def search_with_filters(self, source: str = None, destination: str = None,
                           airline: str = None, max_price: float = None,
                           max_stops: int = None, case_sensitive: bool = False) -> pd.DataFrame:
        """
        Advanced search with multiple filters.

        Args:
            source (str, optional): Source city
            destination (str, optional): Destination city
            airline (str, optional): Airline name
            max_price (float, optional): Maximum price
            max_stops (int, optional): Maximum number of stops
            case_sensitive (bool): Whether to perform case-sensitive search

        Returns:
            pd.DataFrame: Filtered records
        """
        if self.data is None:
            raise ValueError("No data loaded")

        result = self.data.copy()

        if source:
            if not case_sensitive:
                result = result[result['Source'].str.lower() == source.lower()]
            else:
                result = result[result['Source'] == source]

        if destination:
            if not case_sensitive:
                result = result[result['Destination'].str.lower() == destination.lower()]
            else:
                result = result[result['Destination'] == destination]

        if airline:
            if not case_sensitive:
                result = result[result['Airline'].str.lower() == airline.lower()]
            else:
                result = result[result['Airline'] == airline]

        if max_price is not None:
            result = result[result['Price'] <= max_price]

        if max_stops is not None:
            result = result[result['Total_Stops'] <= max_stops]

        return result

    def get_statistics(self) -> Dict:
        """
        Get basic statistics about the dataset.

        Returns:
            Dict: Dictionary containing various statistics
        """
        if self.data is None:
            raise ValueError("No data loaded")

        stats = {
            'total_records': len(self.data),
            'unique_sources': self.data['Source'].nunique(),
            'unique_destinations': self.data['Destination'].nunique(),
            'unique_airlines': self.data['Airline'].nunique(),
            'price_range': {
                'min': self.data['Price'].min(),
                'max': self.data['Price'].max(),
                'average': round(self.data['Price'].mean(), 2)
            },
            'airlines': self.data['Airline'].unique().tolist(),
            'sources': self.data['Source'].unique().tolist(),
            'destinations': self.data['Destination'].unique().tolist()
        }

        return stats
