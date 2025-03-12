from app.models.base_model import BaseModel
from app.extensions import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @staticmethod
    def validate_name(self, name):
        if not name or not isinstance(name, str) or len(name) > 50:
            raise ValueError("Amenity's name must be a non-empty string <= 50 characters")

    def update(self, data):
        if 'name' in data:
            self.validate_name(data['name'])
        super().update(data)
