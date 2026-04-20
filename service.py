import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BASE_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode"

BASE_URL = os.getenv("BASE_URL") or DEFAULT_BASE_URL

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def build_url(postcode: str) -> str:
    return f"{BASE_URL}/{postcode}"


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