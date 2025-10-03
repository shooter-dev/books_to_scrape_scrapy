# -*- coding: utf-8 -*-
"""
Routes API pour les statistiques des livres
----------
API routes for book statistics
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from api_books.src.config.database import get_database_session
from api_books.src.use_cases.stats_use_case import StatsUseCase

router = APIRouter(
    prefix="/stats",
    tags=["statistics"]
)


@router.get("/average-price")
async def get_average_price(db: Session = Depends(get_database_session)):
    """
    Récupère le prix moyen de tous les livres
    ----------
    Retrieve average price of all books
    """
    result = StatsUseCase.get_average_price(db)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }


@router.get("/price-range")
async def get_price_range(db: Session = Depends(get_database_session)):
    """
    Récupère la fourchette de prix (min et max)
    ----------
    Retrieve price range (min and max)
    """
    result = StatsUseCase.get_price_range(db)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }


@router.get("/top-categories")
async def get_top_categories(
    limit: int = Query(10, ge=1, le=50, description="Nombre de catégories à retourner / Number of categories to return"),
    db: Session = Depends(get_database_session)
):
    """
    Récupère les catégories les plus représentées
    ----------
    Retrieve top categories with most books
    """
    result = StatsUseCase.get_top_categories(db, limit=limit)

    if not result["success"]:
        if result["error_type"] == "validation_error":
            raise HTTPException(status_code=400, detail=result["message"])
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }


@router.get("/rating-distribution")
async def get_rating_distribution(db: Session = Depends(get_database_session)):
    """
    Récupère la distribution des notes avec pourcentages
    ----------
    Retrieve rating distribution with percentages
    """
    result = StatsUseCase.get_rating_distribution(db)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }


@router.get("/category/{category}")
async def get_category_stats(
    category: str,
    db: Session = Depends(get_database_session)
):
    """
    Récupère les statistiques détaillées d'une catégorie spécifique
    ----------
    Retrieve detailed statistics for a specific category
    """
    result = StatsUseCase.get_category_stats(db, category)

    if not result["success"]:
        if result["error_type"] == "validation_error":
            raise HTTPException(status_code=400, detail=result["message"])
        elif result["error_type"] == "not_found":
            raise HTTPException(status_code=404, detail=result["message"])
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }


@router.get("/overall")
async def get_overall_stats(db: Session = Depends(get_database_session)):
    """
    Récupère les statistiques globales du catalogue
    ----------
    Retrieve overall catalog statistics
    """
    result = StatsUseCase.get_overall_stats(db)

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }
