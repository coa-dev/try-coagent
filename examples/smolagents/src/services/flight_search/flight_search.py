import pandas as pd

class FlightSearchService:
    """
    A class to search airline records based on source and destination.
    """

    def __init__(self):
        self.csv_file_path = "data/flight_dataset.csv"
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
        return result.to_dict('records')

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

        return self.data[mask].to_dict('records')

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

        return self.data[mask].to_dict('records')
