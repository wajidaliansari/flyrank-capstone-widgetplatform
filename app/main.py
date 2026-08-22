"""
Main module for the Widget Platform API.
"""
import random
import requests
from fastapi import FastAPI, Depends, HTTPException, Request, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Depends, HTTPException
from collections import Counter

from app.database import engine, SessionLocal, Base
from app import models, schemas

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# 1. FIRST, CREATE THE APP
app = FastAPI(
    title="Embeddable Widget & Lead-Capture Platform",
    description="Backend API for managing widgets and capturing leads."
)

# Configure CORS to allow requests from any external customer website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this would be restricted. For this capstone, "*" is standard.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Rate Limiting based on the user's IP address
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Dependency to get the DB session for our endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    """
    Root endpoint to verify the server is running.
    """
    return {"message": "Widget Platform API is running!"}

@app.post("/widgets/", response_model=schemas.WidgetResponse)
def create_widget(widget: schemas.WidgetCreate, db: Session = Depends(get_db)):
    """
    Create a new widget for a specific tenant.
    """
    # 1. Convert the Pydantic schema into a SQLAlchemy model
    db_widget = models.Widget(
        name=widget.name, 
        widget_type=widget.widget_type, 
        tenant_id=widget.tenant_id
    )
    
    # 2. Add it to the database session and save it
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    
    # 3. Return the newly created widget
    return db_widget

def get_geolocation(ip_address: str):
    """
    Enrichment chain: Try Provider A, fallback to Provider B.
    """
    # For local testing, 127.0.0.1 won't work, so we'll mock a public IP if it's local
    if ip_address == "127.0.0.1":
        ip_address = "8.8.8.8" 

    # Try Provider A (ip-api.com)
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("country"), data.get("city")
    except requests.RequestException:
        pass  # Provider A failed, move to fallback

    # Try Provider B (ipapi.co)
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            if "error" not in data:
                return data.get("country_name"), data.get("city")
    except requests.RequestException:
        pass  # Provider B failed

    # If all providers fail, return None without crashing
    return None, None

def send_email_notification(email: str):
    """
    Simulated side effect. If this fails, the main request must still succeed.
    """
    print(f"--> Attempting to send welcome email to {email}...")
    try:
        # In a real app, you'd call an SMTP server like Mailpit here.
        # We will simulate a random failure just to prove it's safe.
        if random.choice([True, False]):
            raise Exception("Fake SMTP server timeout!")
        print("--> Email sent successfully!")
    except Exception as e:
        print(f"--> SIDE EFFECT FAILED: {e}. (But the lead was still saved!)")

# NOTICE: Only ONE submit_lead function here, strictly without the trailing slash!
@app.post("/submissions")
@limiter.limit("5/minute")  
def submit_lead(
    submission: schemas.SubmissionCreate, 
    request: Request, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """
    Public endpoint to capture leads from external websites.
    """
    if submission.honeypot_field:
        return {"message": "Lead captured successfully!"}

    if "@" not in submission.email:
        raise HTTPException(status_code=400, detail="Invalid email format provided.")

    client_ip = request.client.host
    country, city = get_geolocation(client_ip)

    db_submission = models.Submission(
        widget_id=submission.widget_id,
        name=submission.name,
        email=submission.email,
        country=country,
        city=city
    )
    
    db.add(db_submission)
    db.commit()
    
    # Trigger the safe side effect in the background
    background_tasks.add_task(send_email_notification, submission.email)
    
    return {"message": "Lead captured successfully!"}

@app.get("/widgets/{widget_id}/config")
def get_widget_config(widget_id: int, response: Response, db: Session = Depends(get_db)):
    """
    Public endpoint to serve widget configuration to external websites.
    Must be heavily cached!
    """
    widget = db.query(models.Widget).filter(models.Widget.id == widget_id).first()
    
    if not widget or not widget.is_active:
        raise HTTPException(status_code=404, detail="Widget not found or disabled.")

    # Set cache headers (e.g., cache for 5 minutes)
    response.headers["Cache-Control"] = "public, max-age=300"
    
    return {
        "id": widget.id,
        "name": widget.name,
        "type": widget.widget_type,
        "tenant_id": widget.tenant_id
    }

@app.get("/widgets/{widget_id}/dashboard", response_model=schemas.DashboardResponse)
def get_widget_dashboard(widget_id: int, db: Session = Depends(get_db)):
    # 1. Fetch all submissions for this specific widget
    submissions = db.query(models.Submission).filter(models.Submission.widget_id == widget_id).all()
    
    # 2. Handle empty states gracefully
    if not submissions:
        return {
            "total_submissions": 0,
            "geo_breakdown": {},
            "recent_leads": []
        }
    
    # 3. Calculate basic analytics
    total = len(submissions)
    
    # Extract countries, ignoring None values, and count them
    countries = [sub.country for sub in submissions if sub.country]
    geo_stats = dict(Counter(countries))
    
    # 4. Return the structured dashboard data
    return {
        "total_submissions": total,
        "geo_breakdown": geo_stats,
        "recent_leads": submissions
    }