from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext
import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Users ─────────────────────────────────────────────────────────────────────
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 500):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role or "client",
        agency_id=user.agency_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, data: dict):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    for key, value in data.items():
        if key == "password" and value:
            setattr(user, "hashed_password", pwd_context.hash(value))
        elif key != "password":
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# ── Agencies ──────────────────────────────────────────────────────────────────
def create_agency(db: Session, data: schemas.AgencyCreate, head_agent_id: int):
    agency = models.Agency(
        name=data.name,
        address=data.address,
        license_number=data.license_number,
        head_agent_id=head_agent_id,
    )
    db.add(agency)
    db.commit()
    db.refresh(agency)
    # link head agent to agency
    db.query(models.User).filter(models.User.id == head_agent_id).update({"agency_id": agency.id})
    db.commit()
    return agency

def get_agencies(db: Session):
    return db.query(models.Agency).options(joinedload(models.Agency.head_agent)).all()

def get_agency(db: Session, agency_id: int):
    return db.query(models.Agency).options(joinedload(models.Agency.head_agent), joinedload(models.Agency.members)).filter(models.Agency.id == agency_id).first()

def update_agency(db: Session, agency_id: int, data: schemas.AgencyUpdate):
    agency = db.query(models.Agency).filter(models.Agency.id == agency_id).first()
    if not agency:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(agency, key, value)
    db.commit()
    db.refresh(agency)
    return agency

def verify_agency(db: Session, agency_id: int, status: str, reason: str = None):
    agency = db.query(models.Agency).filter(models.Agency.id == agency_id).first()
    if not agency:
        return None
    agency.status = status
    if reason:
        agency.rejection_reason = reason
    db.commit()
    db.refresh(agency)
    return agency

def add_agent_to_agency(db: Session, agency_id: int, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).update({"agency_id": agency_id})
    db.commit()

# ── Properties ────────────────────────────────────────────────────────────────
def get_properties(db: Session, location: str = None, min_price: float = None,
                   max_price: float = None, prop_type: str = None, agent_id: int = None):
    q = db.query(models.Property).options(joinedload(models.Property.agent))
    if location:
        q = q.filter(models.Property.location.ilike(f"%{location}%"))
    if min_price is not None:
        q = q.filter(models.Property.price >= min_price)
    if max_price is not None:
        q = q.filter(models.Property.price <= max_price)
    if prop_type:
        q = q.filter(models.Property.type == prop_type)
    if agent_id:
        q = q.filter(models.Property.agent_id == agent_id)
    return q.all()

def get_property(db: Session, property_id: int):
    return db.query(models.Property).options(joinedload(models.Property.agent)).filter(models.Property.id == property_id).first()

def create_property(db: Session, prop: schemas.PropertyCreate):
    db_prop = models.Property(**prop.dict())
    db.add(db_prop)
    db.commit()
    db.refresh(db_prop)
    return db_prop

def update_property(db: Session, property_id: int, data: dict):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        return None
    for key, value in data.items():
        setattr(prop, key, value)
    db.commit()
    db.refresh(prop)
    return prop

def delete_property(db: Session, property_id: int):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if prop:
        db.delete(prop)
        db.commit()

def assign_property(db: Session, property_id: int, agent_id: int):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        return None
    prop.agent_id = agent_id
    prop.status = "active"
    db.commit()
    db.refresh(prop)
    return prop

def unassign_property(db: Session, property_id: int):
    prop = db.query(models.Property).filter(models.Property.id == property_id).first()
    if not prop:
        return None
    prop.agent_id = None
    prop.status = "unassigned"
    db.commit()
    db.refresh(prop)
    return prop

# ── Appointments ──────────────────────────────────────────────────────────────
def _appt_query(db: Session):
    return db.query(models.Appointment).options(
        joinedload(models.Appointment.client),
        joinedload(models.Appointment.agent),
        joinedload(models.Appointment.property),
    )

def get_appointments(db: Session, user_role: str, user_id: int):
    q = _appt_query(db)
    if user_role == "sub_agent":
        return q.filter(models.Appointment.agent_id == user_id).all()
    elif user_role == "client":
        return q.filter(models.Appointment.client_id == user_id).all()
    return q.all()  # admin / head_agent see all

def get_appointment(db: Session, appt_id: int):
    return _appt_query(db).filter(models.Appointment.id == appt_id).first()

def create_appointment(db: Session, appt: schemas.AppointmentCreate, client_id: int):
    # auto-assign agent from property
    prop = db.query(models.Property).filter(models.Property.id == appt.property_id).first()
    agent_id = prop.agent_id if prop else None
    db_appt = models.Appointment(
        property_id=appt.property_id,
        client_id=client_id,
        agent_id=agent_id,
        date_time=appt.date_time,
        notes=appt.notes,
    )
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return _appt_query(db).filter(models.Appointment.id == db_appt.id).first()

def update_appointment(db: Session, appt_id: int, update: schemas.AppointmentUpdate):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if appt:
        if update.status is not None:    appt.status = update.status
        if update.agent_id is not None:  appt.agent_id = update.agent_id
        if update.agent_notes is not None: appt.agent_notes = update.agent_notes
        if update.date_time is not None: appt.date_time = update.date_time
        db.commit()
        db.refresh(appt)
    return appt

def add_appointment_feedback(db: Session, appt_id: int, feedback: schemas.AppointmentFeedback):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if appt:
        appt.feedback_status = feedback.feedback_status
        appt.feedback_notes = feedback.feedback_notes
        appt.status = "completed"
        db.commit()
        db.refresh(appt)
    return appt

def delete_appointment(db: Session, appt_id: int):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if appt:
        db.delete(appt)
        db.commit()

# ── Leads ─────────────────────────────────────────────────────────────────────
def get_leads(db: Session, agent_id: int = None):
    q = db.query(models.Lead).options(joinedload(models.Lead.property))
    if agent_id:
        # leads for properties assigned to this agent
        assigned_ids = [p.id for p in db.query(models.Property.id).filter(models.Property.agent_id == agent_id)]
        q = q.filter(models.Lead.property_id.in_(assigned_ids))
    return q.order_by(models.Lead.created_at.desc()).all()

def create_lead(db: Session, lead: schemas.LeadCreate, visitor_id: int = None):
    db_lead = models.Lead(
        property_id=lead.property_id,
        visitor_id=visitor_id,
        inquiry_text=lead.inquiry_text,
        visitor_name=lead.visitor_name,
        visitor_email=lead.visitor_email,
        visitor_phone=lead.visitor_phone,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def update_lead(db: Session, lead_id: int, update: schemas.LeadUpdate):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        lead.status = update.status
        db.commit()
        db.refresh(lead)
    return lead

def delete_lead(db: Session, lead_id: int):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if lead:
        db.delete(lead)
        db.commit()

# ── AI Knowledge ──────────────────────────────────────────────────────────────
def get_knowledge_entries(db: Session, category: str = None):
    q = db.query(models.AIKnowledge)
    if category:
        q = q.filter(models.AIKnowledge.category == category)
    return q.order_by(models.AIKnowledge.created_at.desc()).all()

def create_knowledge_entry(db: Session, entry: schemas.AIKnowledgeCreate):
    db_entry = models.AIKnowledge(**entry.dict())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def update_knowledge_entry(db: Session, entry_id: int, data: dict):
    entry = db.query(models.AIKnowledge).filter(models.AIKnowledge.id == entry_id).first()
    if entry:
        for k, v in data.items():
            setattr(entry, k, v)
        db.commit()
        db.refresh(entry)
    return entry

def delete_knowledge_entry(db: Session, entry_id: int):
    entry = db.query(models.AIKnowledge).filter(models.AIKnowledge.id == entry_id).first()
    if entry:
        db.delete(entry)
        db.commit()

# ── Analytics ─────────────────────────────────────────────────────────────────
def get_platform_stats(db: Session):
    from sqlalchemy import func
    total_users = db.query(models.User).count()
    total_properties = db.query(models.Property).count()
    active_properties = db.query(models.Property).filter(models.Property.status == "active").count()
    total_appointments = db.query(models.Appointment).count()
    pending_appointments = db.query(models.Appointment).filter(models.Appointment.status == "pending").count()
    total_agencies = db.query(models.Agency).count()
    pending_agencies = db.query(models.Agency).filter(models.Agency.status == "pending").count()
    clients = db.query(models.User).filter(models.User.role == "client").count()
    sub_agents = db.query(models.User).filter(models.User.role == "sub_agent").count()
    head_agents = db.query(models.User).filter(models.User.role == "head_agent").count()
    total_leads = db.query(models.Lead).count()
    return {
        "total_users": total_users,
        "clients": clients,
        "sub_agents": sub_agents,
        "head_agents": head_agents,
        "total_properties": total_properties,
        "active_properties": active_properties,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
        "total_agencies": total_agencies,
        "pending_agencies": pending_agencies,
        "total_leads": total_leads,
    }

def get_agent_stats(db: Session, agent_id: int):
    from datetime import datetime, timezone
    props = db.query(models.Property).filter(models.Property.agent_id == agent_id).count()
    appts = db.query(models.Appointment).filter(models.Appointment.agent_id == agent_id).all()
    total_appts = len(appts)
    completed = sum(1 for a in appts if a.feedback_status == "completed")
    no_shows = sum(1 for a in appts if a.feedback_status == "no_show")
    pending = sum(1 for a in appts if a.status == "pending")
    confirmed = sum(1 for a in appts if a.status == "confirmed")
    leads = db.query(models.Lead).filter(
        models.Lead.property_id.in_(
            [p.id for p in db.query(models.Property).filter(models.Property.agent_id == agent_id)]
        )
    ).count()
    attendance_rate = round((completed / total_appts * 100) if total_appts > 0 else 0, 1)
    return {
        "assigned_properties": props,
        "total_appointments": total_appts,
        "completed": completed,
        "no_shows": no_shows,
        "pending": pending,
        "confirmed": confirmed,
        "leads": leads,
        "attendance_rate": attendance_rate,
    }
