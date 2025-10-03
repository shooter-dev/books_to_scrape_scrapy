FROM python:3.11-slim

# Métadonnées du conteneur
# Container metadata
LABEL maintainer="ShooterDev"
LABEL description="API FastAPI pour exposer les données scrapées / FastAPI API to expose scraped data"

# Définir le répertoire de travail
# Set working directory
WORKDIR /app

# Installer les dépendances système
# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances Python
# Copy Python dependencies file
COPY requirement.txt .

# Installer les dépendances Python
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip

# Installer FastAPI et ses dépendances si le fichier requirement.txt est vide
# Install FastAPI and dependencies if requirement.txt is empty
RUN if [ ! -s requirement.txt ]; then \
    pip install --no-cache-dir fastapi uvicorn psycopg2-binary sqlalchemy pydantic; \
    else \
    pip install --no-cache-dir -r requirement.txt; \
    fi

# Installer psycopg2 pour PostgreSQL
# Install psycopg2 for PostgreSQL
RUN pip install --no-cache-dir psycopg2-binary

# Copier le code source de l'application
# Copy application source code
COPY . .

# Définir les variables d'environnement
# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Créer un utilisateur non-root pour la sécurité
# Create non-root user for security
RUN groupadd -r apiuser && useradd -r -g apiuser apiuser
RUN chown -R apiuser:apiuser /app
USER apiuser

# Exposer le port pour l'API FastAPI
# Expose port for FastAPI API
EXPOSE 8000

# Vérification de santé du conteneur
# Container health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Commande par défaut pour lancer l'API
# Default command to run the API
CMD ["uvicorn", "api_books.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]