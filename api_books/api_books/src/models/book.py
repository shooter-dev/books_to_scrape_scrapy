from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, func
from api_books.src.config.database import Base

class Book(Base):
    """
    Modèle SQLAlchemy pour représenter un livre dans la base de données
    ----------
    SQLAlchemy model to represent a book in the database
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    price = Column(Numeric(10, 2))
    availability = Column(String(50))
    rating = Column(String(20), index=True)
    url = Column(Text, unique=True)
    image_url = Column(Text)
    description = Column(Text)
    category = Column(String(100), index=True)
    upc = Column(String(50), unique=True)
    product_type = Column(String(100))
    price_excl_tax = Column(Numeric(10, 2))
    price_incl_tax = Column(Numeric(10, 2))
    tax = Column(Numeric(10, 2))
    number_of_reviews = Column(Integer, default=0)
    scraped_at = Column(DateTime, default=func.current_timestamp(), index=True)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def to_dict(self):
        """
        Convertit l'objet Book en dictionnaire
        ----------
        Convert Book object to dictionary
        """
        return {
            "id": self.id,
            "title": self.title,
            "price": float(self.price) if self.price else None,
            "availability": self.availability,
            "rating": self.rating,
            "url": self.url,
            "image_url": self.image_url,
            "description": self.description,
            "category": self.category,
            "upc": self.upc,
            "product_type": self.product_type,
            "price_excl_tax": float(self.price_excl_tax) if self.price_excl_tax else None,
            "price_incl_tax": float(self.price_incl_tax) if self.price_incl_tax else None,
            "tax": float(self.tax) if self.tax else None,
            "number_of_reviews": self.number_of_reviews,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }