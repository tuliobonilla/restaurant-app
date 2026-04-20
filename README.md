# Restaurant Data API

## Overview

This project is a Python application that fetches restaurant data from the Just Eat API using a UK postcode and exposes it through a simple API endpoint.

The goal of this task was to retrieve restaurant data and return only the required fields:

* Name
* Cuisines
* Rating (numeric)
* Address

Initially, I implemented this as a console application. However, after discussing improvements with another developer, I decided to evolve the solution into a simple API, allowing a user to pass a postcode dynamically and receive the results in JSON format.

This made the solution more flexible and closer to how real-world systems are built.

---

## How to build, install and run

1. Clone the repository

git clone https://github.com/tuliobonilla/restaurant-app
cd restaurant-app

2. Create and activate a virtual environment

python -m venv venv

On Windows PowerShell:

.\venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. (Optional) Create a `.env` file

POSTCODE=BS14DJ
BASE_URL=https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode

If the `.env` file is not provided, the application will still work using default values.

5. Run the application (API server)

python app.py

6. Call the API

Example:

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

* `data` contains the list of restaurants (limited to the first 10)
* `error` will contain an error message if something fails, otherwise it will be `null`

---

## Assumptions

* The API response contains a `restaurants` list
* Each restaurant includes the required fields
* The rating is taken from `rating.starRating`
* Only the first 10 restaurants should be returned
* The API is available and responds correctly for valid UK postcodes

---

## Challenges and learning process

While building this solution, I faced several issues and improved the code step by step. I tried to keep the process incremental and learn from each problem.

### API returning 403 instead of 200

When I first called the API, I received a `403 Forbidden` response.

After investigating, I learned that some APIs require proper headers to simulate a real browser request. I fixed this by adding headers like `User-Agent` and `Accept`.

This helped me better understand how HTTP requests work beyond just calling an endpoint.

---

### Address formatting issues

Some addresses returned by the API contained line breaks and extra commas, which made the output messy.

To fix this, I created a dedicated function (`format_address`) to:

* remove line breaks
* clean extra commas
* format everything into a single readable string

---

### Cuisines format was not straightforward

The cuisines field is a list of objects, not a simple string.

Initially, printing it directly resulted in unreadable output. I created a helper function (`format_cuisines`) to extract and join the cuisine names into a readable format.

---

### Handling errors properly

I added a `try/except` block to handle:

* network issues
* timeouts
* API errors

I also used `response.raise_for_status()` to convert HTTP errors into exceptions.

This made the application more robust and closer to production-style code.

---

### Avoiding crashes with missing data

Instead of accessing dictionary values directly, I used `.get()` to avoid runtime errors if some fields are missing in the response.

---

### Using environment variables

I introduced a `.env` file to store configuration such as the postcode and base URL.

I also added default values to ensure the application still works even if the `.env` file is missing.

---

### Evolving from console app to API

After discussing the solution with another developer, I realized that exposing the data through an API would be a more flexible approach.

Instead of hardcoding the postcode, I implemented an endpoint where the user can pass it dynamically:

/restaurants?postcode=XXXX

This change made the solution more reusable and closer to real-world backend applications.

---

### Separating responsibilities into different files

As the project grew, I refactored the code into multiple files to improve readability and structure:

* API layer (handling requests)
* service layer (fetching data from external API)
* formatting layer (data transformation)

This helped me better understand separation of concerns.

---

### JSON field order issue

When returning the API response, I noticed that the fields were not in the same order as requested in the assignment.

Since dictionaries do not always guarantee order depending on how they are built, I explicitly structured the response to ensure the fields appear in this order:

Name → Cuisines → Rating → Address

---

## Improvements I would make

* Add type hints to improve code clarity and maintainability
* Add unit tests
* Add retry logic for API calls
* Improve logging (for example, saving logs to a file)
* Validate API responses more thoroughly
* Add pagination or configurable result limits
* Containerize the application using Docker
* Build a simple frontend to consume the API

---

## Project structure

restaurant-app/
├── app.py
├── service.py
├── formatters.py
├── main.py
├── README.md
├── requirements.txt
└── .env
