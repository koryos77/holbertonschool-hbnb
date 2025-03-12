from app.persistence.repository import SQLAlchemyRepository
from app.models.amenities import Amenity


class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
    
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.add(amenity)
        return amenity
    
    def update_amenity(self, amenity_data, amenity_id):
        amenity = self.get(amenity_id)
        amenity.update(amenity_data)
        return amenity