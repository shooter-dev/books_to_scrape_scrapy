from fastapi import FastAPI
from api_books.src.routes.book_route import router as book_router
from api_books.src.routes.stats_route import router as stats_router
from api_books.src.config.database import engine, Base

# Les tables seront créées automatiquement lors de la première connexion
# Tables will be created automatically on first connection

app = FastAPI(
    title="API Books",
    description="""
    API pour gérer les livres scrapés avec statistiques avancées
    ----------
    API to manage scraped books with advanced statistics

    ## Fonctionnalités / Features:
    - 📚 Gestion des livres / Books management
    - 📊 Statistiques avancées / Advanced statistics
    - 🔍 Recherche par catégorie et note / Search by category and rating
    - 💰 Prix en centimes pour précision maximale / Prices in cents for maximum precision
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Inclusion des routes / Include routes
app.include_router(book_router)
app.include_router(stats_router)



@app.get("/health", tags=["health"])
async def health_check():
    """
    Vérification de l'état de santé de l'API
    ----------
    API health check
    """
    return {"status": "healthy", "service": "api_books"}