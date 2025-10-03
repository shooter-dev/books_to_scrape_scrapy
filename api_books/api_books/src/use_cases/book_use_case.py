from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from api_books.src.services.book_service import BookService
from api_books.src.repositories.book_repository import BookRepository

class BookUseCase:
    """
    Use case pour orchestrer les opérations liées aux livres
    ----------
    Use case to orchestrate book-related operations
    """

    @staticmethod
    def get_all_books(db: Session, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère tous les livres avec gestion des erreurs et validation
        ----------
        Retrieve all books with error handling and validation
        """
        try:
            # Validation des paramètres d'entrée
            # Input parameter validation
            if page < 1:
                raise ValueError("Le numéro de page doit être supérieur à 0 / Page number must be greater than 0")

            if page_size < 1 or page_size > 100:
                raise ValueError("La taille de page doit être entre 1 et 100 / Page size must be between 1 and 100")

            # Injection des dépendances
            # Dependency injection
            book_repository = BookRepository(db)
            book_service = BookService(book_repository)

            # Exécution de la logique métier
            # Execute business logic
            result = book_service.get_all_books(page=page, page_size=page_size)

            return {
                "success": True,
                "data": result,
                "message": "Livres récupérés avec succès / Books retrieved successfully"
            }

        except ValueError as e:
            return {
                "success": False,
                "data": None,
                "message": str(e),
                "error_type": "validation_error"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }

    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Dict[str, Any]:
        """
        Récupère un livre par son ID avec gestion des erreurs
        ----------
        Retrieve a book by ID with error handling
        """
        try:
            # Validation de l'ID
            # ID validation
            if not isinstance(book_id, int) or book_id <= 0:
                raise ValueError("L'ID du livre doit être un entier positif / Book ID must be a positive integer")

            # Injection des dépendances
            # Dependency injection
            book_repository = BookRepository(db)
            book_service = BookService(book_repository)

            # Exécution de la logique métier
            # Execute business logic
            book_data = book_service.get_book_by_id(book_id)

            if book_data is None:
                return {
                    "success": False,
                    "data": None,
                    "message": f"Livre avec l'ID {book_id} non trouvé / Book with ID {book_id} not found",
                    "error_type": "not_found"
                }

            return {
                "success": True,
                "data": book_data,
                "message": "Livre récupéré avec succès / Book retrieved successfully"
            }

        except ValueError as e:
            return {
                "success": False,
                "data": None,
                "message": str(e),
                "error_type": "validation_error"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }

    @staticmethod
    def get_books_by_category(db: Session, category: str, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Récupère les livres par catégorie
        ----------
        Retrieve books by category
        """
        try:
            # Validation des paramètres
            # Parameter validation
            if not category or not category.strip():
                raise ValueError("La catégorie ne peut pas être vide / Category cannot be empty")

            if page < 1:
                raise ValueError("Le numéro de page doit être supérieur à 0 / Page number must be greater than 0")

            if page_size < 1 or page_size > 100:
                raise ValueError("La taille de page doit être entre 1 et 100 / Page size must be between 1 and 100")

            # Injection des dépendances
            # Dependency injection
            book_repository = BookRepository(db)
            book_service = BookService(book_repository)

            # Exécution de la logique métier
            # Execute business logic
            result = book_service.get_books_by_category(category, page=page, page_size=page_size)

            return {
                "success": True,
                "data": result,
                "message": f"Livres de la catégorie '{category}' récupérés avec succès / Books from category '{category}' retrieved successfully"
            }

        except ValueError as e:
            return {
                "success": False,
                "data": None,
                "message": str(e),
                "error_type": "validation_error"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }