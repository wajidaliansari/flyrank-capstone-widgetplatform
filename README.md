# Embeddable Widget & Lead-Capture Platform

A backend platform allowing customers to create embeddable widgets, capture leads via cross-origin requests, and view analytics. Built by Wajid Ali Ansari.

## Architecture
[Widget Owner] -> (Dashboard API) -> [FastAPI + SQLite]
[Public Website] -> (Widget Config) -> [FastAPI + SQLite]
[Website Visitor] -> (Submit Form) -> [FastAPI + SQLite] -> (Background Email Task)

## How to Run Locally
1. Install dependencies: `pip install -r requirements.txt`
2. Start the server: `uvicorn app.main:app --reload`
3. Serve the test site: `python -m http.server 5500`

## Seed Instructions
Use the Swagger UI at `http://127.0.0.1:8000/docs` to send a POST request to `/widgets/` to create your first widget. 

## Limitations
* Email notifications are simulated in the console logs (no real SMTP server is connected).
* Geo-location relies on free third-party APIs which may hit rate limits.