# -*- coding: utf-8 -*-
from datetime import datetime
import scrapy

from books_to_scrape.items import BookItem
from books_to_scrape.loaders import BookLoader


class BooksSpider(scrapy.Spider):
    """
    Spider pour scraper les livres de books.toscrape.com avec détails complets
    ----------
    Spider to scrape books from books.toscrape.com with complete details
    """
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {'data.csv': {'format': 'csv'}},
    }

    def parse(self, response):
        """
        Parse la page principale et navigue vers chaque livre
        ----------
        Parse main page and navigate to each book
        """
        books = response.css('article.product_pod')

        for book in books:
            book_url = book.css('h3 a::attr(href)').get()
            if book_url:
                # Suivre le lien vers la page détaillée du livre
                # Follow link to detailed book page
                yield response.follow(book_url, self.parse_book_details)

        # Pagination - suivre la page suivante
        # Pagination - follow next page
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_book_details(self, response):
        """
        Parse les détails complets d'un livre en utilisant ItemLoader
        ----------
        Parse complete details of a book using ItemLoader
        """
        # Créer le loader pour cet item
        # Create loader for this item
        loader = BookLoader(item=BookItem(), response=response)

        # Informations de base
        # Basic information
        loader.add_css('title', 'h1::text')
        loader.add_css('price', 'p.price_color::text')
        loader.add_css('rating', 'p.star-rating::attr(class)')

        # Disponibilité (extraire tout le texte)
        # Availability (extract all text)
        loader.add_css('availability', 'p.instock.availability::text')

        # URL et image
        # URL and image
        loader.add_value('url', response.url)
        image_url = response.css('div.item.active img::attr(src)').get()
        if image_url:
            loader.add_value('image_url', response.urljoin(image_url))

        # Description
        # Description
        description = response.css('#product_description + p::text').get()
        if not description:
            description = response.css('article.product_page p::text').get()
        if description:
            loader.add_value('description', description)

        # Catégorie (breadcrumb)
        # Category (breadcrumb)
        loader.add_css('category', 'ul.breadcrumb li:nth-last-child(2) a::text')

        # Informations du tableau produit
        # Product table information
        product_info = {}
        table_rows = response.css('table.table tr')
        for row in table_rows:
            key = row.css('th::text').get()
            value = row.css('td::text').get()
            if key and value:
                product_info[key.strip()] = value.strip()

        # Ajouter les détails du produit
        # Add product details
        if 'UPC' in product_info:
            loader.add_value('upc', product_info['UPC'])
        if 'Product Type' in product_info:
            loader.add_value('product_type', product_info['Product Type'])
        if 'Price (excl. tax)' in product_info:
            loader.add_value('price_excl_tax', product_info['Price (excl. tax)'])
        if 'Price (incl. tax)' in product_info:
            loader.add_value('price_incl_tax', product_info['Price (incl. tax)'])
        if 'Tax' in product_info:
            loader.add_value('tax', product_info['Tax'])
        if 'Number of reviews' in product_info:
            loader.add_value('number_of_reviews', product_info['Number of reviews'])

        # Timestamp de scraping
        # Scraping timestamp
        loader.add_value('scraped_at', datetime.now())

        # Charger et retourner l'item
        # Load and return item
        yield loader.load_item()