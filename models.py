from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import validates
from datetime import datetime

from app import db


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    street_address = Column(String(50))
    description = Column(String(250))

    def __str__(self):
        return self.name

class Review(db.Model):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    restaurant = Column(Integer, ForeignKey('restaurant.id', ondelete="CASCADE"))
    user_name = Column(String(30))
    rating = Column(Integer)
    review_text = Column(String(500))
    review_date = Column(DateTime)

    @validates('rating')
    def validate_rating(self, key, value):
        assert value is None or (1 <= value <= 5)
        return value

    def __str__(self):
        return f"{self.user_name}: {self.review_date:%x}"
    
class ImageRecord(db.Model):
    __tablename__ = 'images'

    id           = Column(Integer, primary_key=True)
    red_pixels   = Column(Integer, nullable=False)
    green_pixels = Column(Integer, nullable=False)
    blue_pixels  = Column(Integer, nullable=False)
    width        = Column(Integer, nullable=False)
    height       = Column(Integer, nullable=False)
    filename     = Column(String(255), nullable=False)
    image_data   = Column(LargeBinary, nullable=False)   # <— Blob de la imagen
    created_at   = Column(DateTime)

    @validates('red_pixels', 'green_pixels', 'blue_pixels', 'width', 'height')
    def validate_non_negative(self, key, value):
        assert value >= 0, f"{key} no puede ser negativo"
        return value

    def __repr__(self):
        return (f"<ImageRecord id={self.id} size={self.width}x{self.height} "
                f"pixels=({self.red_pixels},{self.green_pixels},{self.blue_pixels})>")