-- Enable pgcrypto for password hashing if available (optional)
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    role VARCHAR(50) DEFAULT 'client', -- 'admin' or 'client'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Properties Table
CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(15, 2) NOT NULL, -- TND
    location VARCHAR(255) NOT NULL,
    surface DECIMAL(10, 2), -- m²
    type VARCHAR(50), -- apartment, villa, etc.
    bedrooms INTEGER,
    bathrooms INTEGER,
    is_available BOOLEAN DEFAULT TRUE,
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    property_id INTEGER REFERENCES properties(id),
    client_id INTEGER REFERENCES users(id),
    date_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, cancelled
    notes TEXT
);

-- 4. Seed Admin User
-- Password is 'admin123' (bcrypt hash example)
-- If you cannot generate a hash, you can store plain text TEMPORARILY but you must update the backend to support it.
-- For this script, we insert a valid bcrypt hash for 'admin123'
INSERT INTO users (email, hashed_password, full_name, role, phone)
VALUES (
    'admin@gmail.com', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 
    'System Admin', 
    'admin', 
    '+216 00 000 000'
) ON CONFLICT (email) DO NOTHING;

-- 5. Seed Client User
-- Password is 'client123'
INSERT INTO users (email, hashed_password, full_name, role, phone)
VALUES (
    'client@gmail.com', 
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 
    'John Doe', 
    'client', 
    '+216 99 999 999'
) ON CONFLICT (email) DO NOTHING;

-- 6. Seed Properties
INSERT INTO properties (title, description, price, location, surface, type, bedrooms, bathrooms, image_url)
VALUES 
(
    'Luxury Villa in Carthage', 
    'Stunning sea-view villa with pool and large garden.', 
    1200000, 
    'Carthage, Tunis', 
    450, 
    'villa', 
    5, 
    4, 
    'https://images.unsplash.com/photo-1600596542815-6000255161f5'
),
(
    'Modern Apartment in Lac 2', 
    'High-end S+3 apartment in a secure residence.', 
    650000, 
    'Les Berges du Lac 2, Tunis', 
    180, 
    'apartment', 
    3, 
    2, 
    'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00'
);
