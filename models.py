from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import validates
from datetime import datetime

from app import db

    
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