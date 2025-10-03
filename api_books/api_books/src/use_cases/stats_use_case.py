# -*- coding: utf-8 -*-
"""
Use cases pour orchestrer les opérations de statistiques
----------
Use cases to orchestrate statistics operations
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from api_books.src.services.stats_service import StatsService
from api_books.src.repositories.book_repository import BookRepository


class StatsUseCase:
    """
    Use case pour orchestrer les opérations liées aux statistiques
    ----------
    Use case to orchestrate statistics-related operations
    """

    @staticmethod
    def get_average_price(db: Session) -> Dict[str, Any]:
        """
        Récupère le prix moyen des livres
        ----------
        Retrieve average price of books
        """
        try:
            book_repository = BookRepository(db)
            stats_service = StatsService(book_repository)
            result = stats_service.get_average_price()

            return {
                "success": True,
                "data": result,
                "message": "Prix moyen calculé avec succès / Average price calculated successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }

    @staticmethod
    def get_price_range(db: Session) -> Dict[str, Any]:
        """
        Récupère la fourchette de prix
        ----------
        Retrieve price range
        """
        try:
            book_repository = BookRepository(db)
            stats_service = StatsService(book_repository)
            result = stats_service.get_price_range()

            return {
                "success": True,
                "data": result,
                "message": "Fourchette de prix récupérée avec succès / Price range retrieved successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }

    @staticmethod
    def get_top_categories(db: Session, limit: int = 10) -> Dict[str, Any]:
        """
        Récupère les catégories les plus représentées
        ----------
        Retrieve top categories
        """
        try:
            if limit < 1 or limit > 50:
                raise ValueError("La limite doit être entre 1 et 50 / Limit must be between 1 and 50")

            book_repository = BookRepository(db)
            stats_service = StatsService(book_repository)
            result = stats_service.get_top_categories(limit=limit)

            return {
                "success": True,
                "data": result,
                "message": "Top catégories récupérées avec succès / Top categories retrieved successfully"
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
    def get_rating_distribution(db: Session) -> Dict[str, Any]:
        """
        Récupère la distribution des notes
        ----------
        Retrieve rating distribution
        """
        try:
            book_repository = BookRepository(db)
            stats_service = StatsService(book_repository)
            result = stats_service.get_rating_distribution()

            return {
                "success": True,
                "data": result,
                "message": "Distribution des notes récupérée avec succès / Rating distribution retrieved successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }

    @staticmethod
    def get_category_stats(db: Session, category: str) -> Dict[str, Any]:
        """
        Récupère les statistiques d'une catégorie
        ----------
        Retrieve category statistics
        """
        try:
            if not category or not category.strip():
                raise ValueError("La catégorie ne peut pas être vide / Category cannot be empty")

            book_repository = BookRepository(db)
            stats_service = StatsService(book_repository)
            result = stats_service.get_category_stats(category)

            if result is None:
                return {
                    "success": False,
                    "data": None,
                    "message": f"Catégorie '{category}' non trouvée ou vide / Category '{category}' not found or empty",
                    "error_type": "not_found"
                }

            return {
                "success": True,
                "data": result,
                "message": f"Statistiques de la catégorie '{category}' récupérées avec succès / Category '{category}' statistics retrieved successfully"
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
    def get_overall_stats(db: Session) -> Dict[str, Any]:
        """
        Récupère les statistiques globales
        ----------
        Retrieve overall statistics
        """
        try:
            book_repository = BookRepository(db)
            stats_service = StatsService(book_repository)
            result = stats_service.get_overall_stats()

            return {
                "success": True,
                "data": result,
                "message": "Statistiques globales récupérées avec succès / Overall statistics retrieved successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Erreur interne du serveur / Internal server error: {str(e)}",
                "error_type": "server_error"
            }
