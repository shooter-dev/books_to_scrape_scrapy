FROM python:3.11-slim

# Métadonnées du conteneur
# Container metadata
LABEL maintainer="ShooterDev"
LABEL description="Scrapy application pour scraper books.toscrape.com / Scrapy application to scrape books.toscrape.com"

# Définir le répertoire de travail
# Set working directory
WORKDIR /app

# Installer les dépendances système nécessaires pour Scrapy et cron
# Install system dependencies required for Scrapy and cron
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    curl \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances Python
# Copy Python dependencies file
COPY requirement.txt .

# Installer les dépendances Python
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt

# Installer postgresql-client pour pg_isready et pg_dump
# Install postgresql-client for pg_isready and pg_dump
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copier le code source de l'application
# Copy application source code
COPY . .

# Définir les variables d'environnement
# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Exposer le port pour les métriques ou API (optionnel)
# Expose port for metrics or API (optional)
EXPOSE 6080

# Commande par défaut pour lancer le conteneur avec cron
# Default command to run container with cron
CMD ["scrapy", "crawl", "books" ]