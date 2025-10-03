from typing import List, Optional, Dict, Any
from api_books.src.repositories.book_repository import BookRepository
from api_books.src.models.book import Book

class BookService:
    """
    Service pour la logique métier des livres
    ----------
    Service for book business logic
    """

    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def get_all_books(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère tous les livres avec pagination et métadonnées
        ----------
        Retrieve all books with pagination and metadata
        """
        # Calcul des paramètres de pagination
        # Calculate pagination parameters
        skip = (page - 1) * page_size
        limit = page_size

        # Récupération des données
        # Data retrieval
        books = self.book_repository.get_all_books(skip=skip, limit=limit)
        total_count = self.book_repository.get_total_books_count()

        # Calcul des métadonnées de pagination
        # Calculate pagination metadata
        total_pages = (total_count + page_size - 1) // page_size
        has_next = page < total_pages
        has_previous = page > 1

        return {
            "books": [book.to_dict() for book in books],
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_count,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_previous": has_previous
            }
        }

    def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupère un livre par son ID avec validation
        ----------
        Retrieve a book by ID with validation
        """
        if book_id <= 0:
            raise ValueError("L'ID du livre doit être un entier positif / Book ID must be a positive integer")

        book = self.book_repository.get_book_by_id(book_id)

        if book is None:
            return None

        return book.to_dict()

    def get_books_by_category(self, category: str, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les livres par catégorie
        ----------
        Retrieve books by category
        """
        if not category or not category.strip():
            raise ValueError("La catégorie ne peut pas être vide / Category cannot be empty")

        skip = (page - 1) * page_size
        books = self.book_repository.get_books_by_category(category.strip(), skip=skip, limit=page_size)

        return {
            "books": [book.to_dict() for book in books],
            "category": category.strip(),
            "total_found": len(books)
        }

    def get_books_by_rating(self, rating: str, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les livres par note
        ----------
        Retrieve books by rating
        """
        valid_ratings = ["One", "Two", "Three", "Four", "Five"]

        if rating not in valid_ratings:
            raise ValueError(f"Note invalide. Valeurs acceptées: {', '.join(valid_ratings)} / Invalid rating. Accepted values: {', '.join(valid_ratings)}")

        skip = (page - 1) * page_size
        books = self.book_repository.get_books_by_rating(rating, skip=skip, limit=page_size)

        return {
            "books": [book.to_dict() for book in books],
            "rating": rating,
            "total_found": len(books)
        }