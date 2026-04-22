# Restaurant Data API

## Overview

This project is a Python application that fetches restaurant data from the Just Eat API using a UK postcode and exposes it through a simple API endpoint.

The goal of this task was to retrieve restaurant data and return only the required fields:

- Name
- Cuisines
- Rating (numeric)
- Address

Initially, I implemented this as a console application to better understand the API structure and data format. After refining the solution and discussing improvements with another developer, I evolved it into a simple API, allowing users to pass a postcode dynamically and receive results in JSON format.

This made the solution more flexible and closer to how real-world backend services are designed.

---

## How to build, install and run

### Clone the repository

git clone https://github.com/tuliobonilla/restaurant-app
cd restaurant-app

### Create and activate a virtual environment

python -m venv venv

On Windows PowerShell:

.\venv\Scripts\Activate.ps1

### Install dependencies

pip install -r requirements.txt

### Create a .env file (optional)

POSTCODE=BS14DJ
BASE_URL=https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode

If the .env file is not provided, the application will still work using default values.

### Run the application

python app.py

### Call the API

http://127.0.0.1:5000/restaurants?postcode=BS14DJ

---

## API Response Format

The API returns a JSON response in the following format:

{
  "data": [
    {
      "name": "...",
      "cuisines": "...",
      "rating": ...,
      "address": "..."
    }
  ],
  "error": null
}

- data contains the list of restaurants (limited to the first 10)
- error will contain an error message if something fails, otherwise it will be null

---

## Assumptions

- The API response contains a restaurants list
- Each restaurant includes the required fields
- The rating is taken from rating.starRating
- Only the first 10 restaurants should be returned
- The API is available and responds correctly for valid UK postcodes

---

## Challenges and learning process

### API returning 403 instead of 200

When I first called the API, I received a 403 Forbidden response. After investigating, I learned that some APIs require proper headers to simulate a real browser request. I fixed this by adding headers like User-Agent and Accept.

### Address formatting issues

Some addresses returned by the API contained line breaks and extra commas. I created a function (format_address) to clean and format the address into a single readable string.

### Cuisines format was not straightforward

The cuisines field is returned as a list of objects rather than a simple string. I created a helper function (format_cuisines) to extract and join cuisine names into a readable format.

### Handling errors properly

I added a try/except block to handle network issues, timeouts, and API errors. I also used response.raise_for_status() to convert HTTP errors into exceptions.

### Avoiding crashes with missing data

To avoid runtime errors when fields are missing, I used .get() instead of direct dictionary access.

### Using environment variables

I introduced a .env file to store configuration such as postcode and base URL, along with default values so the application still works without it.

### Evolving from console app to API

After discussing improvements with another developer I refactored the application into an API. Instead of hardcoding the postcode, the application now exposes an endpoint /restaurants?postcode=XXXX.

### Separating responsibilities

The project was refactored into multiple layers: app.py (API), service.py (data fetching), formatters.py (data transformation), and models.py (data structure).

### Introducing structured typing

I introduced a typed model using TypedDict (Restaurant), defining the structure of the final response and reducing reliance on generic types like Any.

### JSON field order issue

I ensured that the response fields are returned in the required order: Name → Cuisines → Rating → Address.

---

## Improvements I would make

- Limit results directly at the external API level (if supported)
- Add unit tests
- Add retry logic for API calls
- Improve logging (e.g., writing logs to a file)
- Validate API responses more strictly
- Add pagination or configurable result limits
- Containerize the application using Docker
- Build a simple frontend to consume the API

---

## Project structure

restaurant-app/
├── app.py
├── service.py
├── formatters.py
├── models.py
├── main.py
├── README.md
├── requirements.txt
└── .env