from pydantic import BaseModel
from typing import List, Dict, Optional

class WidgetCreate(BaseModel):
    name: str
    widget_type: str
    tenant_id: str  # In a real app, this comes from an auth token. We'll require it in the payload for now.

class WidgetResponse(BaseModel):
    id: int
    name: str
    widget_type: str
    tenant_id: str
    is_active: bool

    class Config:
        from_attributes = True  # This tells Pydantic to read data from our SQLAlchemy model

class SubmissionCreate(BaseModel):
    widget_id: int
    name: str
    email: str
    honeypot_field: str | None = None  # Hidden field to trap bots

class SubmissionResponse(BaseModel):
    id: int
    name: str
    email: str
    country: Optional[str] = None
    city: Optional[str] = None

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    total_submissions: int
    geo_breakdown: Dict[str, int]
    recent_leads: List[SubmissionResponse]