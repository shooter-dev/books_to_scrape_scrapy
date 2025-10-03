from fastapi import FastAPI
from api_books.src.routes.book_route import router as book_router
from api_books.src.config.database import engine, Base

# Les tables seront créées automatiquement lors de la première connexion
# Tables will be created automatically on first connection

app = FastAPI(
    title="API Books",
    description="API pour gérer les livres scrapés / API to manage scraped books",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Inclusion des routes
app.include_router(book_router)



@app.get("/health", tags=["health"])
async def health_check():
    """
    Vérification de l'état de santé de l'API
    ----------
    API health check
    """
    return {"status": "healthy", "service": "api_books"}