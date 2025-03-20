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
        """Update an amenity"""
        amenity = self.model.query.get(amenity_id)
        if not amenity:
            return None
        
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        
        self.add(amenity)
        return amenity
