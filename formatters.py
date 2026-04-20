from typing import Any


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