from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import validates
from datetime import datetime

from app import db

    
class ImageRecord(db.Model):
    __tablename__ = 'images'

    id               = Column(Integer, primary_key=True)
    usuario          = Column(String(255), nullable=False)  # Nuevo campo para el usuario
    red_pixels       = Column(Integer, nullable=False)
    green_pixels     = Column(Integer, nullable=False)
    blue_pixels      = Column(Integer, nullable=False)
    width            = Column(Integer, nullable=False)
    height           = Column(Integer, nullable=False)
    filename         = Column(String(255), nullable=False)
    image_data_original = Column(LargeBinary, nullable=False)  # Imagen original
    image_data_R     = Column(LargeBinary, nullable=False)  # Imagen con canal rojo
    image_data_G     = Column(LargeBinary, nullable=False)  # Imagen con canal verde
    image_data_B     = Column(LargeBinary, nullable=False)  # Imagen con canal azul
    image_data_BN    = Column(LargeBinary, nullable=False)  # Imagen en blanco y negro
    image_data_Pix   = Column(LargeBinary, nullable=False)  # Imagen pixelada
    created_at       = Column(DateTime)

    @validates('red_pixels', 'green_pixels', 'blue_pixels', 'width', 'height')
    def validate_non_negative(self, key, value):
        assert value >= 0, f"{key} no puede ser negativo"
        return value

    def __repr__(self):
        return (f"<ImageRecord id={self.id} usuario={self.usuario} size={self.width}x{self.height} "
                f"pixels=({self.red_pixels},{self.green_pixels},{self.blue_pixels})>")