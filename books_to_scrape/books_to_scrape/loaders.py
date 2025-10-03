# -*- coding: utf-8 -*-
"""
ItemLoaders personnalisés pour le scraping de livres
----------
Custom ItemLoaders for book scraping
"""

import re
from datetime import datetime
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose, Identity


def strip_whitespace(value):
    """
    Supprime les espaces en début et fin de chaîne
    ----------
    Strip leading and trailing whitespace from string
    """
    if value:
        return value.strip()
    return value


def parse_price(value):
    """
    Extrait et convertit le prix en centimes (entier)
    ----------
    Extract and convert price to cents (integer)
    """
    if not value:
        return None
    try:
        # Supprime le symbole £ et convertit en centimes
        # Remove £ symbol and convert to cents
        cleaned = re.sub(r'[£,]', '', value)
        price_float = float(cleaned)
        return int(price_float * 100)  # Conversion en centimes
    except (ValueError, TypeError):
        return None


def parse_rating(value):
    """
    Extrait la note depuis la classe CSS
    ----------
    Extract rating from CSS class
    """
    if not value:
        return None
    # Extrait "One", "Two", "Three", "Four", "Five" depuis "star-rating One"
    # Extract "One", "Two", "Three", "Four", "Five" from "star-rating One"
    match = re.search(r'star-rating (\w+)', value)
    return match.group(1) if match else None


def parse_availability(value):
    """
    Extrait la disponibilité en stock
    ----------
    Extract stock availability
    """
    if not value:
        return None
    # Cherche le nombre d'exemplaires disponibles
    # Search for number of available copies
    match = re.search(r'(\d+) available', value)
    if match:
        return f"{match.group(1)} available"
    # Sinon retourne juste "In stock" ou autre
    # Otherwise return just "In stock" or other
    return value.strip()


def parse_number(value):
    """
    Convertit en entier
    ----------
    Convert to integer
    """
    if not value:
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


def get_current_timestamp():
    """
    Retourne le timestamp actuel
    ----------
    Return current timestamp
    """
    return datetime.now()


class BookLoader(ItemLoader):
    """
    ItemLoader personnalisé pour charger les données de livres avec validation et nettoyage
    ----------
    Custom ItemLoader to load book data with validation and cleaning
    """
    # Par défaut, prendre la première valeur et nettoyer les espaces
    # By default, take first value and clean whitespace
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(strip_whitespace)

    # Processeurs spécifiques pour les champs
    # Specific processors for fields
    title_in = MapCompose(strip_whitespace)
    title_out = TakeFirst()

    price_in = MapCompose(strip_whitespace)
    price_out = Compose(TakeFirst(), parse_price)

    price_excl_tax_in = MapCompose(strip_whitespace)
    price_excl_tax_out = Compose(TakeFirst(), parse_price)

    price_incl_tax_in = MapCompose(strip_whitespace)
    price_incl_tax_out = Compose(TakeFirst(), parse_price)

    tax_in = MapCompose(strip_whitespace)
    tax_out = Compose(TakeFirst(), parse_price)

    rating_in = MapCompose(str.strip)
    rating_out = Compose(TakeFirst(), parse_rating)

    availability_in = MapCompose(str.strip)
    availability_out = Compose(Join(' '), parse_availability)

    description_in = MapCompose(strip_whitespace)
    description_out = TakeFirst()

    category_in = MapCompose(strip_whitespace)
    category_out = TakeFirst()

    upc_in = MapCompose(strip_whitespace)
    upc_out = TakeFirst()

    product_type_in = MapCompose(strip_whitespace)
    product_type_out = TakeFirst()

    number_of_reviews_in = MapCompose(strip_whitespace)
    number_of_reviews_out = Compose(TakeFirst(), parse_number)

    url_out = TakeFirst()
    image_url_out = TakeFirst()

    # Le timestamp est généré, pas extrait - utilise Identity pour passer la valeur telle quelle
    # Timestamp is generated, not extracted - use Identity to pass value as-is
    scraped_at_in = Identity()
    scraped_at_out = TakeFirst()
