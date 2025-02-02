import os
import csv
import numpy as np
from typing import Dict, List, Tuple

# Global dictionaries to store post office data and their locations.
POST_OFFICES: Dict[str, dict] = {}
POST_OFFICES_LOCATIONS: List[Tuple[float, float]] = []


def init_data(csv_path: str = "Post_offices.csv") -> None:
    """
    Initialize post office data from a CSV file. This function populates the global
    variables POST_OFFICES and POST_OFFICES_LOCATIONS.

    Args:
        csv_path (str): The file path to the CSV file containing post office data.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
    """
    global POST_OFFICES, POST_OFFICES_LOCATIONS

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # Read CSV file with '|' as delimiter
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            try:
                lat = float(row["lat"])
                lng = float(row["lng"])
            except (ValueError, KeyError) as e:
                # Skip the row if there's an error converting latitude or longitude
                continue

            key = f"{lat}:{lng}"
            POST_OFFICES[key] = row

    # Build list of locations from the post offices data
    POST_OFFICES_LOCATIONS = [
        (float(post_office["lat"]), float(post_office["lng"]))
        for post_office in POST_OFFICES.values()
    ]


def get_nearest(lat: float, lng: float) -> dict:
    """
    Calculate and return the nearest post office to the given latitude and longitude.

    Args:
        lat (float): The latitude of the reference location.
        lng (float): The longitude of the reference location.

    Returns:
        dict: A dictionary containing data for the nearest post office.

    Raises:
        ValueError: If post office data has not been initialized.
    """
    if not POST_OFFICES_LOCATIONS:
        raise ValueError("Post offices data is not initialized. Call init_data() first.")

    # Convert list of locations into a NumPy array for vectorized operations
    locations_array = np.array(POST_OFFICES_LOCATIONS)
    reference_point = np.array([lat, lng])

    # Calculate Euclidean distances from the reference point to each post office
    distances = np.linalg.norm(locations_array - reference_point, axis=1)
    min_index = np.argmin(distances)
    nearest_lat, nearest_lng = locations_array[min_index]

    key = f"{nearest_lat}:{nearest_lng}"
    return POST_OFFICES[key]


# Initialize data when this module is imported or run.
init_data()
