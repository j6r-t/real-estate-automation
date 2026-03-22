from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    HEAD_AGENT = "head_agent"
    SUB_AGENT = "sub_agent"
    CLIENT = "client"

class PropertyType(str, enum.Enum):
    APARTMENT = "apartment"
    VILLA = "villa"
    HOUSE = "house"
    STUDIO = "studio"
    COMMERCIAL = "commercial"
    LAND = "land"

class AgencyStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class PropertyStatus(str, enum.Enum):
    UNASSIGNED = "unassigned"
    ACTIVE = "active"
    SOLD = "sold"

class LeadStatus(str, enum.Enum):
    NEW = "new"
    CONTACTED = "contacted"
    LOST = "lost"

# ── Agency ──────────────────────────────────────────────────────────────────
class Agency(Base):
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    license_number = Column(String, unique=True)
    status = Column(String, default=AgencyStatus.PENDING.value)
    trust_score = Column(Float, default=100.0)
    rejection_reason = Column(Text, nullable=True)
    head_agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    head_agent = relationship("User", back_populates="managed_agency", foreign_keys=[head_agent_id])
    members = relationship("User", back_populates="agency", foreign_keys="User.agency_id")
    properties = relationship("Property", back_populates="agency")

# ── User ─────────────────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone = Column(String)
    role = Column(String, default=UserRole.CLIENT.value)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agency = relationship("Agency", back_populates="members", foreign_keys=[agency_id])
    managed_agency = relationship("Agency", back_populates="head_agent", foreign_keys="Agency.head_agent_id")
    appointments = relationship("Appointment", back_populates="client", foreign_keys="Appointment.client_id")
    agent_appointments = relationship("Appointment", back_populates="agent", foreign_keys="Appointment.agent_id")
    assigned_properties = relationship("Property", back_populates="agent", foreign_keys="Property.agent_id")

# ── Property ──────────────────────────────────────────────────────────────────
class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    location = Column(String, index=True, nullable=False)
    surface = Column(Float)
    type = Column(String, default=PropertyType.APARTMENT.value)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    is_available = Column(Boolean, default=True)
    status = Column(String, default=PropertyStatus.UNASSIGNED.value)
    image_url = Column(String)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=True)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agency = relationship("Agency", back_populates="properties")
    agent = relationship("User", back_populates="assigned_properties", foreign_keys=[agent_id])
    appointments = relationship("Appointment", back_populates="property")
    leads = relationship("Lead", back_populates="property")

# ── Appointment ───────────────────────────────────────────────────────────────
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    client_id = Column(Integer, ForeignKey("users.id"))
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    date_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="pending")  # pending | confirmed | cancelled | completed
    notes = Column(Text)
    agent_notes = Column(Text)
    feedback_status = Column(String, nullable=True)   # completed | no_show
    feedback_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    property = relationship("Property", back_populates="appointments")
    client = relationship("User", back_populates="appointments", foreign_keys=[client_id])
    agent = relationship("User", back_populates="agent_appointments", foreign_keys=[agent_id])

# ── Lead ──────────────────────────────────────────────────────────────────────
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    inquiry_text = Column(Text)
    status = Column(String, default=LeadStatus.NEW.value)  # new | contacted | lost
    visitor_name = Column(String, nullable=True)
    visitor_email = Column(String, nullable=True)
    visitor_phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    property = relationship("Property", back_populates="leads")
    visitor = relationship("User", foreign_keys=[visitor_id])

# ── AI Knowledge ──────────────────────────────────────────────────────────────
class AIKnowledge(Base):
    __tablename__ = "ai_knowledge"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String, default="general")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
