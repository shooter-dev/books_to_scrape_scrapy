import datetime
from datetime import datetime
import re

import scrapy


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
        Parse les détails complets d'un livre
        ----------
        Parse complete details of a book
        """
        # Informations de base
        # Basic information
        title = response.css('h1::text').get()
        price_text = response.css('p.price_color::text').get()
        price = float(re.sub(r'[£]', '', price_text)) if price_text else None

        # Disponibilité
        # Availability
        availability_text = response.css('p.instock.availability::text').re_first(r'\((\d+) available\)')
        availability = availability_text if availability_text else response.css('p.instock.availability::text').re_first(r'\w+')

        # Rating
        rating_class = response.css('p.star-rating::attr(class)').get()
        rating = re.search(r'star-rating (\w+)', rating_class).group(1) if rating_class else None

        # Image
        image_url = response.css('div.item.active img::attr(src)').get()
        if image_url:
            image_url = response.urljoin(image_url)

        # Description
        description = response.css('#product_description + p::text').get()
        if not description:
            description = response.css('article.product_page p::text').get()

        # Informations du tableau produit
        # Product table information
        product_info = {}
        table_rows = response.css('table.table tr')
        for row in table_rows:
            key = row.css('th::text').get()
            value = row.css('td::text').get()
            if key and value:
                product_info[key.strip()] = value.strip()

        # Catégorie (breadcrumb)
        # Category (breadcrumb)
        category = response.css('ul.breadcrumb li:nth-last-child(2) a::text').get()

        # Construire l'item avec tous les détails
        # Build item with all details
        yield {
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating,
            'url': response.url,
            'image_url': image_url,
            'description': description,
            'category': category,
            # Détails du tableau produit
            # Product table details
            'upc': product_info.get('UPC'),
            'product_type': product_info.get('Product Type'),
            'price_excl_tax': self.parse_price(product_info.get('Price (excl. tax)')),
            'price_incl_tax': self.parse_price(product_info.get('Price (incl. tax)')),
            'tax': self.parse_price(product_info.get('Tax')),
            'number_of_reviews': int(product_info.get('Number of reviews', 0)) if product_info.get('Number of reviews', '0').isdigit() else 0,
            'scraped_at': datetime.now()
        }

    def parse_price(self, price_text):
        """
        Parse et convertit un prix en float
        ----------
        Parse and convert price to float
        """
        if not price_text:
            return None
        try:
            return float(re.sub(r'[£]', '', price_text))
        except (ValueError, TypeError):
            return None