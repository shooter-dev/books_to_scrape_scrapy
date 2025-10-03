from sqlalchemy import Column, Integer, String, Text, DateTime, func
from api_books.src.config.database import Base

class Book(Base):
    """
    Modèle SQLAlchemy pour représenter un livre dans la base de données
    Les prix sont stockés en centimes (INTEGER)
    ----------
    SQLAlchemy model to represent a book in the database
    Prices are stored in cents (INTEGER)
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    price = Column(Integer)  # Prix en centimes / Price in cents
    availability = Column(String(50))
    rating = Column(String(20), index=True)
    url = Column(Text, unique=True)
    image_url = Column(Text)
    description = Column(Text)
    category = Column(String(100), index=True)
    upc = Column(String(50), unique=True)
    product_type = Column(String(100))
    price_excl_tax = Column(Integer)  # Prix HT en centimes / Price excl. tax in cents
    price_incl_tax = Column(Integer)  # Prix TTC en centimes / Price incl. tax in cents
    tax = Column(Integer)  # Taxe en centimes / Tax in cents
    number_of_reviews = Column(Integer, default=0)
    scraped_at = Column(DateTime, default=func.current_timestamp(), index=True)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def to_dict(self):
        """
        Convertit l'objet Book en dictionnaire
        Les prix sont convertis de centimes en euros (float) pour l'API
        ----------
        Convert Book object to dictionary
        Prices are converted from cents to euros (float) for the API
        """
        return {
            "id": self.id,
            "title": self.title,
            "price": round(self.price / 100, 2) if self.price else None,
            "availability": self.availability,
            "rating": self.rating,
            "url": self.url,
            "image_url": self.image_url,
            "description": self.description,
            "category": self.category,
            "upc": self.upc,
            "product_type": self.product_type,
            "price_excl_tax": round(self.price_excl_tax / 100, 2) if self.price_excl_tax else None,
            "price_incl_tax": round(self.price_incl_tax / 100, 2) if self.price_incl_tax else None,
            "tax": round(self.tax / 100, 2) if self.tax else None,
            "number_of_reviews": self.number_of_reviews,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }