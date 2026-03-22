from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import timedelta

import models, schemas, crud, auth as auth_module, email_service
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Luxe Estate API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth Helper ───────────────────────────────────────────────────────────────
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ")[1]
    payload = auth_module.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_email(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_roles(*roles):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail=f"Requires one of: {roles}")
        return current_user
    return checker

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.post("/token")
def login_for_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    token = auth_module.create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=timedelta(hours=24)
    )
    return {"access_token": token, "token_type": "bearer", "role": user.role}

# ── Users ─────────────────────────────────────────────────────────────────────
@app.get("/users/", response_model=List[schemas.User])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, data: dict, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"ok": True}

@app.get("/users/me", response_model=schemas.UserPublic)
def get_me(current_user=Depends(get_current_user)):
    return current_user

# ── Agencies ──────────────────────────────────────────────────────────────────
@app.get("/agencies/", response_model=List[schemas.Agency])
def list_agencies(db: Session = Depends(get_db)):
    return crud.get_agencies(db)

@app.get("/agencies/{agency_id}", response_model=schemas.Agency)
def get_agency(agency_id: int, db: Session = Depends(get_db)):
    agency = crud.get_agency(db, agency_id)
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency

@app.post("/agencies/", response_model=schemas.Agency)
def create_agency(data: schemas.AgencyCreate, current_user=Depends(require_roles("head_agent", "admin")), db: Session = Depends(get_db)):
    return crud.create_agency(db, data, current_user.id)

@app.put("/agencies/{agency_id}", response_model=schemas.Agency)
def update_agency(agency_id: int, data: schemas.AgencyUpdate, db: Session = Depends(get_db)):
    agency = crud.update_agency(db, agency_id, data)
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency

@app.put("/agencies/{agency_id}/verify")
def verify_agency(agency_id: int, body: dict, db: Session = Depends(get_db)):
    status = body.get("status")
    reason = body.get("reason")
    if status not in ("verified", "rejected"):
        raise HTTPException(status_code=400, detail="Status must be 'verified' or 'rejected'")
    agency = crud.verify_agency(db, agency_id, status, reason)
    if not agency:
        raise HTTPException(status_code=404, detail="Agency not found")
    return agency

@app.post("/agencies/{agency_id}/agents")
def add_agent_to_agency(agency_id: int, body: dict, db: Session = Depends(get_db)):
    user_id = body.get("user_id")
    crud.add_agent_to_agency(db, agency_id, user_id)
    return {"ok": True}

@app.get("/agencies/{agency_id}/members", response_model=List[schemas.UserPublic])
def get_agency_members(agency_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.agency_id == agency_id).all()

# ── Properties ────────────────────────────────────────────────────────────────
@app.get("/properties/", response_model=List[schemas.Property])
def list_properties(
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    type: Optional[str] = None,
    agent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_properties(db, location=location, min_price=min_price, max_price=max_price, prop_type=type, agent_id=agent_id)

@app.get("/properties/{property_id}", response_model=schemas.Property)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = crud.get_property(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@app.post("/properties/", response_model=schemas.Property)
def create_property(prop: schemas.PropertyCreate, db: Session = Depends(get_db)):
    return crud.create_property(db, prop)

@app.put("/properties/{property_id}", response_model=schemas.Property)
def update_property(property_id: int, data: dict, db: Session = Depends(get_db)):
    prop = crud.update_property(db, property_id, data)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@app.put("/properties/{property_id}/assign")
def assign_property(property_id: int, body: schemas.PropertyAssign, db: Session = Depends(get_db)):
    prop = crud.assign_property(db, property_id, body.agent_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@app.put("/properties/{property_id}/unassign")
def unassign_property(property_id: int, db: Session = Depends(get_db)):
    prop = crud.unassign_property(db, property_id)
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop

@app.delete("/properties/{property_id}")
def delete_property(property_id: int, db: Session = Depends(get_db)):
    crud.delete_property(db, property_id)
    return {"ok": True}

# ── Appointments ──────────────────────────────────────────────────────────────
@app.get("/appointments/", response_model=List[schemas.Appointment])
def list_appointments(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_appointments(db, current_user.role, current_user.id)

@app.get("/appointments/{appt_id}", response_model=schemas.Appointment)
def get_appointment(appt_id: int, db: Session = Depends(get_db)):
    appt = crud.get_appointment(db, appt_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@app.post("/appointments/", response_model=schemas.Appointment)
def create_appointment(appt: schemas.AppointmentCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_appointment(db, appt, current_user.id)

@app.put("/appointments/{appt_id}", response_model=schemas.Appointment)
def update_appointment(appt_id: int, update: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    appt = crud.get_appointment(db, appt_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    old_status = appt.status
    updated = crud.update_appointment(db, appt_id, update)
    # Email notifications
    if updated and update.status and update.status != old_status and updated.client:
        client = updated.client
        prop_title = updated.property.title if updated.property else "Property"
        agent_name = updated.agent.full_name if updated.agent else "Our team"
        date_str = updated.date_time.strftime("%B %d, %Y at %H:%M")
        if update.status == "confirmed":
            email_service.notify_appointment_confirmed(client.email, client.full_name or "Client", prop_title, date_str, agent_name)
        elif update.status == "cancelled":
            email_service.notify_appointment_cancelled(client.email, client.full_name or "Client", prop_title, date_str, update.agent_notes or "")
    return crud.get_appointment(db, appt_id)

@app.post("/appointments/{appt_id}/feedback", response_model=schemas.Appointment)
def add_appointment_feedback(appt_id: int, feedback: schemas.AppointmentFeedback, db: Session = Depends(get_db)):
    appt = crud.add_appointment_feedback(db, appt_id, feedback)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@app.delete("/appointments/{appt_id}")
def delete_appointment(appt_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db, appt_id)
    return {"ok": True}

# ── Leads ─────────────────────────────────────────────────────────────────────
@app.get("/leads/", response_model=List[schemas.Lead])
def list_leads(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    agent_id = current_user.id if current_user.role == "sub_agent" else None
    return crud.get_leads(db, agent_id=agent_id)

@app.post("/leads/", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    visitor_id = None
    if authorization and authorization.startswith("Bearer "):
        payload = auth_module.decode_token(authorization.split(" ")[1])
        if payload:
            user = crud.get_user_by_email(db, payload.get("sub"))
            if user:
                visitor_id = user.id
    return crud.create_lead(db, lead, visitor_id)

@app.put("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead(lead_id: int, update: schemas.LeadUpdate, db: Session = Depends(get_db)):
    lead = crud.update_lead(db, lead_id, update)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    crud.delete_lead(db, lead_id)
    return {"ok": True}

# ── Analytics ─────────────────────────────────────────────────────────────────
@app.get("/analytics/platform")
def platform_analytics(db: Session = Depends(get_db)):
    return crud.get_platform_stats(db)

@app.get("/analytics/agent/{agent_id}")
def agent_analytics(agent_id: int, db: Session = Depends(get_db)):
    return crud.get_agent_stats(db, agent_id)

# ── AI Knowledge ──────────────────────────────────────────────────────────────
@app.get("/ai-knowledge/", response_model=List[schemas.AIKnowledge])
def list_knowledge(category: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.get_knowledge_entries(db, category=category)

@app.post("/ai-knowledge/", response_model=schemas.AIKnowledge)
def create_knowledge(entry: schemas.AIKnowledgeCreate, db: Session = Depends(get_db)):
    return crud.create_knowledge_entry(db, entry)

@app.put("/ai-knowledge/{entry_id}", response_model=schemas.AIKnowledge)
def update_knowledge(entry_id: int, data: dict, db: Session = Depends(get_db)):
    entry = crud.update_knowledge_entry(db, entry_id, data)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@app.delete("/ai-knowledge/{entry_id}")
def delete_knowledge(entry_id: int, db: Session = Depends(get_db)):
    crud.delete_knowledge_entry(db, entry_id)
    return {"ok": True}
