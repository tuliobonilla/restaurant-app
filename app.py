import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from formatters import format_restaurant
from service import fetch_restaurants

load_dotenv()

DEFAULT_POSTCODE = "BS14DJ"
MAX_RESULTS = 10

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

app = Flask(__name__)
app.json.sort_keys = False


@app.get("/restaurants")
def get_restaurants():
    postcode = request.args.get("postcode", "").strip() or os.getenv("POSTCODE") or DEFAULT_POSTCODE

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