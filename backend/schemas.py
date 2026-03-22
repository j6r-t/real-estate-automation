from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ── User Schemas ──────────────────────────────────────────────────────────────
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "client"
    agency_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class UserPublic(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    role: str
    agency_id: Optional[int] = None
    class Config:
        from_attributes = True

# ── Agency Schemas ────────────────────────────────────────────────────────────
class AgencyBase(BaseModel):
    name: str
    address: Optional[str] = None
    license_number: Optional[str] = None

class AgencyCreate(AgencyBase):
    pass

class AgencyUpdate(AgencyBase):
    status: Optional[str] = None
    rejection_reason: Optional[str] = None

class Agency(AgencyBase):
    id: int
    status: str
    trust_score: float
    rejection_reason: Optional[str] = None
    head_agent_id: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True

class AgencyWithDetails(Agency):
    head_agent: Optional[UserPublic] = None
    member_count: Optional[int] = 0
    property_count: Optional[int] = 0

# ── Property Schemas ──────────────────────────────────────────────────────────
class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    location: str
    surface: Optional[float] = None
    type: Optional[str] = "apartment"
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    is_available: bool = True
    image_url: Optional[str] = None
    agency_id: Optional[int] = None
    agent_id: Optional[int] = None
    status: Optional[str] = "unassigned"

class PropertyCreate(PropertyBase):
    pass

class Property(PropertyBase):
    id: int
    created_at: datetime
    agent: Optional[UserPublic] = None
    class Config:
        from_attributes = True

class PropertyAssign(BaseModel):
    agent_id: int

# ── Appointment Schemas ───────────────────────────────────────────────────────
class AppointmentBase(BaseModel):
    property_id: int
    date_time: datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    client_id: Optional[int] = None

class AppointmentUpdate(BaseModel):
    status: Optional[str] = None
    agent_id: Optional[int] = None
    agent_notes: Optional[str] = None
    date_time: Optional[datetime] = None

class AppointmentFeedback(BaseModel):
    feedback_status: str   # completed | no_show
    feedback_notes: Optional[str] = None

class Appointment(AppointmentBase):
    id: int
    client_id: int
    agent_id: Optional[int] = None
    status: str
    agent_notes: Optional[str] = None
    feedback_status: Optional[str] = None
    feedback_notes: Optional[str] = None
    created_at: datetime
    client: Optional[UserPublic] = None
    agent: Optional[UserPublic] = None
    class Config:
        from_attributes = True

# ── Lead Schemas ──────────────────────────────────────────────────────────────
class LeadCreate(BaseModel):
    property_id: int
    inquiry_text: Optional[str] = None
    visitor_name: Optional[str] = None
    visitor_email: Optional[str] = None
    visitor_phone: Optional[str] = None

class LeadUpdate(BaseModel):
    status: str  # new | contacted | lost

class Lead(BaseModel):
    id: int
    property_id: int
    visitor_id: Optional[int] = None
    inquiry_text: Optional[str] = None
    status: str
    visitor_name: Optional[str] = None
    visitor_email: Optional[str] = None
    visitor_phone: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# ── AI Knowledge Schemas ──────────────────────────────────────────────────────
class AIKnowledgeBase(BaseModel):
    topic: str
    question: str
    answer: str
    category: Optional[str] = "general"
    is_active: Optional[bool] = True

class AIKnowledgeCreate(AIKnowledgeBase):
    pass

class AIKnowledge(AIKnowledgeBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
