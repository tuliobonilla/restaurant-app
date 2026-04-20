# Restaurant Data Viewer

## Overview

This project is a Python console application that fetches restaurant data from the Just Eat API using a UK postcode.

The goal of this task was to retrieve restaurant data from the API and display only the required fields:

- Name
- Cuisines
- Rating (numeric)
- Address

I chose to build a console application because the brief mentioned that all interface types would be assessed equally, so I focused on making the data retrieval and formatting as clear and reliable as possible.

---

## How to build, install and run

1. Clone the repository

git clone (https://github.com/tuliobonilla/restaurant-app)  
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

5. Run the application

python main.py  

---

## Assumptions

- The API response contains a `restaurants` list
- Each restaurant includes the required fields
- The rating is taken from `rating.starRating`
- Only the first 10 restaurants should be displayed
- A console application is sufficient for this task

---

## Challenges and learning process

While building this solution, I faced several issues and improved the code step by step.

### API returning 403 instead of 200

When I first called the API, I received a `403 Forbidden` response.

After investigating, I understood that the API requires proper headers.  
I fixed this by adding headers like `User-Agent` and `Accept`.

This helped me better understand how HTTP requests work in practice.

---

### Address formatting issues

Some addresses returned by the API contained line breaks and extra commas.

This caused messy output in the console.

To fix this, I created a dedicated function (`format_address`) to:
- remove line breaks
- clean extra commas
- format everything into a single readable line

---

### Cuisines format was not straightforward

The cuisines field is not a simple string but a list of objects.

At first, I tried printing it directly, but it was not readable.

I created a helper function (`format_cuisines`) to extract and join the cuisine names.

---

### Handling errors properly

I added a `try/except` block to handle:
- network issues
- timeouts
- API errors

I also used `response.raise_for_status()` to convert HTTP errors into exceptions.

This made the application more robust.

---

### Avoiding crashes with missing data

I replaced direct dictionary access with `.get()` to prevent the program from breaking if a field is missing.

---

### Improving structure and readability

As I iterated, I started separating responsibilities into functions:

- fetching data from the API
- formatting data
- displaying results

This made the code easier to read and maintain.

---

### Using environment variables

I introduced a `.env` file to store configuration like postcode and base URL.

I also added default values to ensure the application still works if the `.env` file is missing.

---

## Improvements I would make


- Allow the user to enter a postcode dynamically
- Improve address formatting (city and state with same name)
- Add unit tests
- Add retry logic for API calls
- Improve logging (for example, saving logs to a file)
- Validate API responses more thoroughly
- Build a simple web interface
- Allow configuration of how many restaurants to display

---

## Project structure

restaurant-app/  
├── main.py  
├── README.md  
├── requirements.txt  
└── .env
