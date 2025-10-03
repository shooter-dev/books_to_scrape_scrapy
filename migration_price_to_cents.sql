-- Migration script: Convertir les prix de DECIMAL vers INTEGER (centimes)
-- Migration script: Convert prices from DECIMAL to INTEGER (cents)

-- ATTENTION: Ce script doit être exécuté sur une base existante pour migrer les données
-- WARNING: This script must be run on an existing database to migrate data

-- Étape 1: Créer des colonnes temporaires en centimes
-- Step 1: Create temporary columns in cents
ALTER TABLE books ADD COLUMN IF NOT EXISTS price_new INTEGER;
ALTER TABLE books ADD COLUMN IF NOT EXISTS price_excl_tax_new INTEGER;
ALTER TABLE books ADD COLUMN IF NOT EXISTS price_incl_tax_new INTEGER;
ALTER TABLE books ADD COLUMN IF NOT EXISTS tax_new INTEGER;

-- Étape 2: Convertir les valeurs existantes en centimes
-- Step 2: Convert existing values to cents
UPDATE books SET price_new = ROUND(price * 100)::INTEGER WHERE price IS NOT NULL;
UPDATE books SET price_excl_tax_new = ROUND(price_excl_tax * 100)::INTEGER WHERE price_excl_tax IS NOT NULL;
UPDATE books SET price_incl_tax_new = ROUND(price_incl_tax * 100)::INTEGER WHERE price_incl_tax IS NOT NULL;
UPDATE books SET tax_new = ROUND(tax * 100)::INTEGER WHERE tax IS NOT NULL;

-- Étape 3: Supprimer les anciennes colonnes
-- Step 3: Drop old columns
ALTER TABLE books DROP COLUMN IF EXISTS price;
ALTER TABLE books DROP COLUMN IF EXISTS price_excl_tax;
ALTER TABLE books DROP COLUMN IF EXISTS price_incl_tax;
ALTER TABLE books DROP COLUMN IF EXISTS tax;

-- Étape 4: Renommer les nouvelles colonnes
-- Step 4: Rename new columns
ALTER TABLE books RENAME COLUMN price_new TO price;
ALTER TABLE books RENAME COLUMN price_excl_tax_new TO price_excl_tax;
ALTER TABLE books RENAME COLUMN price_incl_tax_new TO price_incl_tax;
ALTER TABLE books RENAME COLUMN tax_new TO tax;

-- Étape 5: Recréer l'index sur le prix
-- Step 5: Recreate index on price
DROP INDEX IF EXISTS idx_books_price;
CREATE INDEX idx_books_price ON books(price);

-- Vérification: Afficher quelques lignes pour valider
-- Verification: Display some rows to validate
SELECT
    title,
    price,
    price_excl_tax,
    price_incl_tax,
    tax
FROM books
LIMIT 5;
