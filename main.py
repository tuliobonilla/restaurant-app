import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

DEFAULT_POSTCODE = "BS14DJ"
DEFAULT_BASE_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode"

BASE_URL = os.getenv("BASE_URL") or DEFAULT_BASE_URL
MAX_RESULTS = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

app = Flask(__name__)


def build_url(postcode: str) -> str:
    return f"{BASE_URL}/{postcode}"


def format_address(address_data: dict[str, Any]) -> str:
    first_line_raw = address_data.get("firstLine", "")
    first_line_parts = [part.strip(" ,") for part in first_line_raw.splitlines() if part.strip()]
    first_line = ", ".join(first_line_parts)

    city = address_data.get("city", "").strip(" ,")
    postal_code = address_data.get("postalCode", "").strip(" ,")

    parts = [first_line, city, postal_code]
    return ", ".join(part for part in parts if part)


def format_cuisines(cuisines_data: list[dict[str, Any]]) -> str:
    cuisine_names = [cuisine.get("name", "") for cuisine in cuisines_data if cuisine.get("name")]
    return ", ".join(cuisine_names)


def format_restaurant(restaurant: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": restaurant.get("name", "N/A"),
        "cuisines": format_cuisines(restaurant.get("cuisines", [])) or "N/A",
        "rating": restaurant.get("rating", {}).get("starRating", "N/A"),
        "address": format_address(restaurant.get("address", {})) or "N/A",
    }


def fetch_restaurants(postcode: str) -> list[dict[str, Any]] | None:
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


@app.get("/restaurants")
def get_restaurants():
    postcode = request.args.get("postcode", "").strip() or DEFAULT_POSTCODE

    logging.info("Fetching restaurant data for postcode %s", postcode)
    restaurants = fetch_restaurants(postcode)

    if restaurants is None:
        return jsonify(
            {
                "data": [],
                "error": "Failed to fetch data from the upstream API.",
            }
        ), 502

    formatted_restaurants = [format_restaurant(restaurant) for restaurant in restaurants[:MAX_RESULTS]]

    return jsonify(
        {
            "data": formatted_restaurants,
            "error": None,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)