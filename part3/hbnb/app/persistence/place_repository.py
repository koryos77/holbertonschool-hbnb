from app.persistence.repository import SQLAlchemyRepository
from app.models.places import Place


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def create_place(self, place_data):
        place = Place(**place_data)
        self.add(place)
        return place

    def update_place(self, place_data, place_id):
        place = self.get(place_id)
        if not place:
            return None
        place.update(place_data)
        return place
