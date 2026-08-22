from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Widget(Base):
    __tablename__ = "widgets"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String, index=True)  # Critical for multi-tenant isolation
    name = Column(String, index=True)
    widget_type = Column(String)  # e.g., 'signup', 'contact', 'popover'
    is_active = Column(Boolean, default=True)

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    widget_id = Column(Integer, index=True)
    name = Column(String)
    email = Column(String)
    # New enrichment fields
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)