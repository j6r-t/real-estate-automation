from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas

# Create Tables
models.Base.metadata.create_all(bind=engine)

def init_db():
    db = SessionLocal()
    
    # 1. Create Admin
    admin = crud.get_user_by_email(db, "admin@luxeestate.com")
    if not admin:
        print("Creating Admin User...")
        admin_data = schemas.UserCreate(
            email="admin@luxeestate.com", password="adminpassword123", full_name="System Admin", 
            role="admin", phone="+216 00 000 000"
        )
        crud.create_user(db, admin_data)

    # 2. Create Head Agent
    head = crud.get_user_by_email(db, "head@luxeestate.com")
    if not head:
        print("Creating Head Agent...")
        head_data = schemas.UserCreate(
            email="head@luxeestate.com", password="password123", full_name="Sarah Connor",
            role="head_agent", phone="+216 11 111 111"
        )
        head = crud.create_user(db, head_data)
        
        # Create Agency for Head Agent
        print("Creating Sample Agency...")
        agency = models.Agency(
            name="Luxe Estate HQ", address="Les Berges du Lac 2, Tunis",
            license_number="AG-2024-001", status="verified",
            head_agent_id=head.id
        )
        db.add(agency)
        db.commit()
        db.refresh(agency)
        
        # Update head agent's agency_id
        head.agency_id = agency.id
        db.commit()

    # 3. Create Sub-Agent from existing 'agent' if migration happened, or new one
    sub = crud.get_user_by_email(db, "agent@luxeestate.com")
    if not sub:
        print("Creating Sub-Agent...")
        sub_data = schemas.UserCreate(
            email="agent@luxeestate.com", password="password123", full_name="John Wick",
            role="sub_agent", phone="+216 22 222 222"
        )
        sub = crud.create_user(db, sub_data)
        
        # Assign to agency if exists
        agency = db.query(models.Agency).first()
        if agency:
            sub.agency_id = agency.id
            db.commit()

    # 4. Seed Properties
    if not db.query(models.Property).first():
        print("Seeding Properties...")
        props = [
            schemas.PropertyCreate(
                title="Luxury Villa in Carthage", description="Stunning sea-view villa with pool.",
                price=1200000, location="Carthage, Tunis", surface=450, type="villa",
                bedrooms=5, bathrooms=4, image_url="https://images.unsplash.com/photo-1600596542815-6000255161f5"
            ),
             schemas.PropertyCreate(
                title="Modern Apartment in Lac 2", description="High-end S+3 apartment.",
                price=650000, location="Les Berges du Lac 2, Tunis", surface=180, type="apartment",
                bedrooms=3, bathrooms=2, image_url="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00"
            )
        ]
        for p in props:
            crud.create_property(db, p)
            
    print("Database Seeded Successfully!")
    db.close()

if __name__ == "__main__":
    init_db()
