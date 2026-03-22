-- ============================================================
-- Migration SQL: Full Platform Restructuring (v2.0)
-- Run this in pgAdmin's Query Tool against your database
-- ============================================================

-- 1. Add new columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR;
ALTER TABLE users ADD COLUMN IF NOT EXISTS agency_id INTEGER;

-- 2. Create agencies table
CREATE TABLE IF NOT EXISTS agencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    address VARCHAR,
    license_number VARCHAR UNIQUE,
    status VARCHAR DEFAULT 'pending',
    trust_score FLOAT DEFAULT 100.0,
    rejection_reason TEXT,
    head_agent_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Add agency FK to users
ALTER TABLE users ADD CONSTRAINT users_agency_id_fkey
    FOREIGN KEY (agency_id) REFERENCES agencies(id);

-- 4. Update user roles (rename old agent → sub_agent)
UPDATE users SET role = 'sub_agent' WHERE role = 'agent';

-- 5. Add new columns to properties table
ALTER TABLE properties ADD COLUMN IF NOT EXISTS agency_id INTEGER REFERENCES agencies(id);
ALTER TABLE properties ADD COLUMN IF NOT EXISTS agent_id INTEGER REFERENCES users(id);
ALTER TABLE properties ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'unassigned';

-- 6. Add new columns to appointments table
ALTER TABLE appointments ADD COLUMN IF NOT EXISTS feedback_status VARCHAR;
ALTER TABLE appointments ADD COLUMN IF NOT EXISTS feedback_notes TEXT;

-- 7. Create leads table
CREATE TABLE IF NOT EXISTS leads (
    id SERIAL PRIMARY KEY,
    visitor_id INTEGER REFERENCES users(id),
    property_id INTEGER NOT NULL REFERENCES properties(id),
    inquiry_text TEXT,
    status VARCHAR DEFAULT 'new',
    visitor_name VARCHAR,
    visitor_email VARCHAR,
    visitor_phone VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- 8. Update properties status from available flag
UPDATE properties SET status = 'active' WHERE is_available = true AND status = 'unassigned';
UPDATE properties SET status = 'sold' WHERE is_available = false;

-- ✅ Done! Restart your uvicorn server after running this migration.
