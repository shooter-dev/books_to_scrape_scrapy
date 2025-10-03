from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from api_books.src.config.database import get_database_session
from api_books.src.use_cases.book_use_case import BookUseCase

router = APIRouter(
    prefix="/books",
    tags=["books"]
)


@router.get("/")
async def get_all_books(
    page: int = Query(1, ge=1, description="Numéro de page / Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Taille de page / Page size"),
    db: Session = Depends(get_database_session)
):
    """
    Récupère tous les livres avec pagination
    ----------
    Retrieve all books with pagination
    """
    result = BookUseCase.get_all_books(db, page=page, page_size=page_size)

    if not result["success"]:
        if result["error_type"] == "validation_error":
            raise HTTPException(status_code=400, detail=result["message"])
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    return {
        "message": result["message"],
        "data": result["data"]
    }


@router.get("/{book_id}")
async def get_book_by_id(
    book_id: int,
    db: Session = Depends(get_database_session)
):
    """
    Récupère un livre par son ID
    ----------
    Retrieve a book by its ID
    """
    result = BookUseCase.get_book_by_id(db, book_id=book_id)

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
