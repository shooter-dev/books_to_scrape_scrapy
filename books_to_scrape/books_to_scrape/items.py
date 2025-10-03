# -*- coding: utf-8 -*-
"""
Définition des Items Scrapy pour le scraping de livres
----------
Scrapy Items definition for book scraping
"""

import scrapy


class BookItem(scrapy.Item):
    """
    Item représentant un livre scrapé avec tous ses détails
    ----------
    Item representing a scraped book with all its details
    """
    # Informations de base
    # Basic information
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()

    # Informations détaillées du produit
    # Detailed product information
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    number_of_reviews = scrapy.Field()

    # Métadonnées
    # Metadata
    scraped_at = scrapy.Field()
