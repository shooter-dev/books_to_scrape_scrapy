# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from psycopg2.extras import RealDictCursor

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksToScrapePostgresPipeline:
    """
    Pipeline pour sauvegarder les items dans PostgreSQL
    ----------
    Pipeline to save items to PostgreSQL
    """

    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        """
        Connexion à la base de données PostgreSQL au démarrage du spider
        ----------
        Connect to PostgreSQL database when spider starts
        """
        try:
            self.connection = psycopg2.connect(**spider.settings.get('DATABASE_SETTINGS'))
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            spider.logger.info("Connexion à PostgreSQL établie / PostgreSQL connection established")
        except Exception as e:
            spider.logger.error(f"Erreur de connexion à PostgreSQL / PostgreSQL connection error: {e}")

    def close_spider(self, spider):
        """
        Fermeture de la connexion à la base de données
        ----------
        Close database connection
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        spider.logger.info("Connexion PostgreSQL fermée / PostgreSQL connection closed")

    def process_item(self, item, spider):
        """
        Traitement et sauvegarde de chaque item
        ----------
        Process and save each item
        """
        try:
            adapter = ItemAdapter(item)

            insert_sql = """
                INSERT INTO books (
                    title, price, availability, rating, url, image_url,
                    description, category, upc, product_type, price_excl_tax,
                    price_incl_tax, tax, number_of_reviews, scraped_at
                ) VALUES (
                    %(title)s, %(price)s, %(availability)s, %(rating)s, %(url)s, %(image_url)s,
                    %(description)s, %(category)s, %(upc)s, %(product_type)s, %(price_excl_tax)s,
                    %(price_incl_tax)s, %(tax)s, %(number_of_reviews)s, %(scraped_at)s
                )
            """

            self.cursor.execute(insert_sql, dict(adapter))
            self.connection.commit()
            spider.logger.debug(f"Item sauvé / Item saved: {adapter.get('title', 'N/A')}")

        except Exception as e:
            self.connection.rollback()
            spider.logger.error(f"Erreur lors de la sauvegarde / Error saving item: {e}")

        return item
