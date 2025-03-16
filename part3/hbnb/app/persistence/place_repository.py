from app.persistence.repository import SQLAlchemyRepository
from app.models.places import Place
from app.extensions import db


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def create_place(self, place_data):
        place = Place(**place_data)
        self.add(place)
        return place

    def update_place(self, place_data, place_id):
        """Update a place"""
        place = self.model.query.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            setattr(place, key, value)

        self.add(place)
        return place
