# -*- coding: utf-8 -*-
"""
Service pour la logique métier des statistiques
----------
Service for statistics business logic
"""

from typing import Dict, Any, Optional
from api_books.src.repositories.book_repository import BookRepository


class StatsService:
    """
    Service dédié aux statistiques sur les livres
    ----------
    Service dedicated to book statistics
    """

    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def get_average_price(self) -> Dict[str, Any]:
        """
        Calcule le prix moyen avec conversion en euros
        ----------
        Calculate average price with conversion to euros
        """
        avg_cents = self.book_repository.get_average_price()
        return {
            "average_price_cents": avg_cents,
            "average_price_euros": round(avg_cents / 100, 2) if avg_cents else None
        }

    def get_price_range(self) -> Dict[str, Any]:
        """
        Retourne la fourchette de prix avec conversion en euros
        ----------
        Return price range with conversion to euros
        """
        price_range = self.book_repository.get_price_range()
        return {
            "min_price_cents": price_range["min_price"],
            "min_price_euros": round(price_range["min_price"] / 100, 2) if price_range["min_price"] else None,
            "max_price_cents": price_range["max_price"],
            "max_price_euros": round(price_range["max_price"] / 100, 2) if price_range["max_price"] else None
        }

    def get_top_categories(self, limit: int = 10) -> Dict[str, Any]:
        """
        Retourne les catégories les plus représentées avec validation
        ----------
        Return top categories with validation
        """
        if limit <= 0 or limit > 50:
            raise ValueError("La limite doit être entre 1 et 50 / Limit must be between 1 and 50")

        categories = self.book_repository.get_top_categories(limit=limit)
        return {
            "top_categories": categories,
            "total_returned": len(categories)
        }

    def get_rating_distribution(self) -> Dict[str, Any]:
        """
        Retourne la distribution des notes avec pourcentages
        ----------
        Return rating distribution with percentages
        """
        distribution = self.book_repository.get_rating_distribution()
        total_books = sum(item["count"] for item in distribution)

        # Ajouter les pourcentages
        # Add percentages
        for item in distribution:
            item["percentage"] = round((item["count"] / total_books * 100), 2) if total_books > 0 else 0

        return {
            "distribution": distribution,
            "total_books": total_books
        }

    def get_category_stats(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Retourne les statistiques détaillées d'une catégorie
        ----------
        Return detailed statistics for a category
        """
        if not category or not category.strip():
            raise ValueError("La catégorie ne peut pas être vide / Category cannot be empty")

        stats = self.book_repository.get_category_stats(category.strip())

        if not stats:
            return None

        # Convertir les prix en euros
        # Convert prices to euros
        stats["avg_price_euros"] = round(stats["avg_price"] / 100, 2) if stats["avg_price"] else None
        stats["min_price_euros"] = round(stats["min_price"] / 100, 2) if stats["min_price"] else None
        stats["max_price_euros"] = round(stats["max_price"] / 100, 2) if stats["max_price"] else None

        return stats

    def get_overall_stats(self) -> Dict[str, Any]:
        """
        Retourne les statistiques globales complètes
        ----------
        Return complete overall statistics
        """
        stats = self.book_repository.get_overall_stats()

        # Convertir les prix en euros
        # Convert prices to euros
        stats["avg_price_euros"] = round(stats["avg_price"] / 100, 2) if stats["avg_price"] else None
        stats["min_price_euros"] = round(stats["min_price"] / 100, 2) if stats["min_price"] else None
        stats["max_price_euros"] = round(stats["max_price"] / 100, 2) if stats["max_price"] else None

        return stats
