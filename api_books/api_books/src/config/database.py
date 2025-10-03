# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configuration PostgreSQL
# PostgreSQL configuration
DATABASE_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
    'database': os.getenv('POSTGRES_DB', 'scrapy_db'),
    'user': os.getenv('POSTGRES_USER', 'scrapy_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'scrapy_password')
}

# Construction de l'URL de connexion PostgreSQL
# PostgreSQL connection URL construction
DATABASE_URL = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# Configuration du moteur SQLAlchemy
# SQLAlchemy engine configuration
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv('DATABASE_DEBUG', 'False').lower() == 'true'
)

# Configuration de la session
# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modeles
# Base for models
Base = declarative_base()

def get_database_session():
    """
    Generateur de session de base de donnees pour l'injection de dependance
    ----------
    Database session generator for dependency injection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()