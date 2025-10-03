from typing import List, Optional
from sqlalchemy.orm import Session
from api_books.src.models.book import Book

class BookRepository:
    """
    Repository pour l'accès aux données des livres
    ----------
    Repository for book data access
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all_books(self, skip: int = 0, limit: int = 100) -> List[Book]:
        """
        Récupère tous les livres avec pagination
        ----------
        Retrieve all books with pagination
        """
        return self.db.query(Book).offset(skip).limit(limit).all()

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """
        Récupère un livre par son ID
        ----------
        Retrieve a book by its ID
        """
        return self.db.query(Book).filter(Book.id == book_id).first()

    def get_total_books_count(self) -> int:
        """
        Compte le nombre total de livres
        ----------
        Count total number of books
        """
        return self.db.query(Book).count()

    def get_books_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Book]:
        """
        Récupère les livres par catégorie
        ----------
        Retrieve books by category
        """
        return self.db.query(Book).filter(Book.category == category).offset(skip).limit(limit).all()

    def get_books_by_rating(self, rating: str, skip: int = 0, limit: int = 100) -> List[Book]:
        """
        Récupère les livres par note
        ----------
        Retrieve books by rating
        """
        return self.db.query(Book).filter(Book.rating == rating).offset(skip).limit(limit).all()