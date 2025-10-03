from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
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

    # ========== Méthodes de statistiques / Statistics methods ==========

    def get_average_price(self) -> Optional[int]:
        """
        Calcule le prix moyen de tous les livres (en centimes)
        ----------
        Calculate average price of all books (in cents)
        """
        result = self.db.query(func.avg(Book.price)).scalar()
        return int(result) if result else None

    def get_price_range(self) -> Dict[str, Optional[int]]:
        """
        Retourne le prix minimum et maximum (en centimes)
        ----------
        Return minimum and maximum price (in cents)
        """
        min_price = self.db.query(func.min(Book.price)).scalar()
        max_price = self.db.query(func.max(Book.price)).scalar()
        return {
            "min_price": min_price,
            "max_price": max_price
        }

    def get_top_categories(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retourne les catégories avec le plus de livres
        ----------
        Return categories with the most books
        """
        results = (
            self.db.query(
                Book.category,
                func.count(Book.id).label('count')
            )
            .group_by(Book.category)
            .order_by(func.count(Book.id).desc())
            .limit(limit)
            .all()
        )
        return [{"category": r.category, "count": r.count} for r in results]

    def get_rating_distribution(self) -> List[Dict[str, Any]]:
        """
        Retourne la distribution des notes
        ----------
        Return rating distribution
        """
        results = (
            self.db.query(
                Book.rating,
                func.count(Book.id).label('count')
            )
            .group_by(Book.rating)
            .order_by(func.count(Book.id).desc())
            .all()
        )
        return [{"rating": r.rating, "count": r.count} for r in results]

    def get_category_stats(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Retourne les statistiques pour une catégorie spécifique
        ----------
        Return statistics for a specific category
        """
        results = (
            self.db.query(
                func.count(Book.id).label('total_books'),
                func.avg(Book.price).label('avg_price'),
                func.min(Book.price).label('min_price'),
                func.max(Book.price).label('max_price')
            )
            .filter(Book.category == category)
            .first()
        )

        if not results or results.total_books == 0:
            return None

        return {
            "category": category,
            "total_books": results.total_books,
            "avg_price": int(results.avg_price) if results.avg_price else None,
            "min_price": results.min_price,
            "max_price": results.max_price
        }

    def get_overall_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques globales
        ----------
        Return overall statistics
        """
        results = (
            self.db.query(
                func.count(Book.id).label('total_books'),
                func.avg(Book.price).label('avg_price'),
                func.min(Book.price).label('min_price'),
                func.max(Book.price).label('max_price'),
                func.count(func.distinct(Book.category)).label('total_categories')
            )
            .first()
        )

        return {
            "total_books": results.total_books or 0,
            "avg_price": int(results.avg_price) if results.avg_price else None,
            "min_price": results.min_price,
            "max_price": results.max_price,
            "total_categories": results.total_categories or 0
        }