import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_POSTCODE = "BS14DJ"
DEFAULT_BASE_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode"

POSTCODE = os.getenv("POSTCODE") or DEFAULT_POSTCODE
BASE_URL = os.getenv("BASE_URL") or DEFAULT_BASE_URL

MAX_RESULTS = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def build_url(postcode):
    return f"{BASE_URL}/{postcode}"


def format_address(address_data):
    first_line_raw = address_data.get("firstLine", "")
    first_line_parts = [part.strip(" ,") for part in first_line_raw.splitlines() if part.strip()]
    first_line = ", ".join(first_line_parts)

    city = address_data.get("city", "").strip(" ,")
    postal_code = address_data.get("postalCode", "").strip(" ,")

    parts = [first_line, city, postal_code]
    return ", ".join(part for part in parts if part)


def format_cuisines(cuisines_data):
    cuisine_names = [cuisine.get("name", "") for cuisine in cuisines_data if cuisine.get("name")]
    return ", ".join(cuisine_names)


def fetch_restaurants(postcode):
    url = build_url(postcode)

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("restaurants", [])
    except requests.exceptions.RequestException as error:
        logging.error("Failed to fetch data from the API: %s", error)
        return None
    except ValueError as error:
        logging.error("Failed to parse API response as JSON: %s", error)
        return None


def display_restaurants(restaurants):
    if not restaurants:
        print("No restaurants found for the provided postcode.")
        return

    results_to_display = min(len(restaurants), MAX_RESULTS)
    print(f"Showing {results_to_display} restaurant(s):")

    for restaurant in restaurants[:MAX_RESULTS]:
        name = restaurant.get("name", "N/A")
        cuisines = format_cuisines(restaurant.get("cuisines", [])) or "N/A"
        rating = restaurant.get("rating", {}).get("starRating", "N/A")
        address = format_address(restaurant.get("address", {})) or "N/A"

        print("-" * 50)
        print(f"Name: {name}")
        print(f"Cuisines: {cuisines}")
        print(f"Rating: {rating}")
        print(f"Address: {address}")


def main():
    logging.info("Fetching restaurant data for postcode %s", POSTCODE)
    restaurants = fetch_restaurants(POSTCODE)

    if restaurants is None:
        print("The application could not retrieve restaurant data.")
        return

    display_restaurants(restaurants)


if __name__ == "__main__":
    main()
