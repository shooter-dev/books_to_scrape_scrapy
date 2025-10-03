-- Script d'initialisation de la base de données PostgreSQL
-- Initialization script for PostgreSQL database

-- Table pour stocker les livres scrapés avec tous les détails
-- Table to store scraped books with all details
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2),
    availability VARCHAR(50),
    rating VARCHAR(20),
    url TEXT UNIQUE,
    image_url TEXT,
    description TEXT,
    category VARCHAR(100),
    upc VARCHAR(50) UNIQUE,
    product_type VARCHAR(100),
    price_excl_tax DECIMAL(10, 2),
    price_incl_tax DECIMAL(10, 2),
    tax DECIMAL(10, 2),
    number_of_reviews INTEGER DEFAULT 0,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Créer un index sur le titre pour améliorer les performances de recherche
-- Create an index on title for better search performance
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);

-- Créer un index sur la catégorie
-- Create an index on category
CREATE INDEX IF NOT EXISTS idx_books_category ON books(category);

-- Créer un index sur la date de scraping
-- Create an index on scraping date
CREATE INDEX IF NOT EXISTS idx_books_scraped_at ON books(scraped_at);

-- Créer un index sur le prix pour les requêtes de tri/filtrage
-- Create an index on price for sorting/filtering queries
CREATE INDEX IF NOT EXISTS idx_books_price ON books(price);

-- Créer un index sur le rating
-- Create an index on rating
CREATE INDEX IF NOT EXISTS idx_books_rating ON books(rating);

-- Fonction pour mettre à jour automatiquement updated_at
-- Function to automatically update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger pour mettre à jour updated_at automatiquement
-- Trigger to automatically update updated_at
CREATE TRIGGER update_books_updated_at
    BEFORE UPDATE ON books
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();