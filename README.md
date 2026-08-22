
<img width="1819" height="926" alt="Screenshot 2026-08-22 142307" src="https://github.com/user-attachments/assets/7c25f158-fe18-4df0-84b6-349414419036" />
<img width="1780" height="917" alt="Screenshot 2026-08-22 142243" src="https://github.com/user-attachments/assets/7b1bae79-b4a5-42b9-bb00-f648a8737d45" />
<img width="1782" height="925" alt="Screenshot 2026-08-22 142225" src="https://github.com/user-attachments/assets/ba4ab498-cd0d-4b6e-be99-699708082eae" />
<img width="1780" height="928" alt="Screenshot 2026-08-22 142324" src="https://github.com/user-attachments/assets/1500e7c5-498a-4af4-84b1-12656af53afa" />
<img width="1838" height="895" alt="Screenshot 2026-08-22 142203" src="https://github.com/user-attachments/assets/a685bb76-b6eb-4f58-9ca3-f217009d6838" />
<img width="916" height="736" alt="Screenshot 2026-08-22 140721" src="https://github.com/user-attachments/assets/6c2021dc-c629-4fe4-b8d0-565ac727dd91" />
<img width="1919" height="1023" alt="Screenshot 2026-08-22 140422" src="https://github.com/user-attachments/assets/31d122dd-77c3-43aa-9432-5c9fbd8d2ca8" />
# Embeddable Widget & Lead-Capture Platform
![Working Widget Demonstration](./widget-demo.png)


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
