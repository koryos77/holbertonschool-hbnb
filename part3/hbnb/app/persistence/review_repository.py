from app.persistence.repository import SQLAlchemyRepository
from app.models.reviews import Review


class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def create_review(self, review_data):
        review = Review(**review_data)
        self.add(review)
        return review

    def update_review(self, review_data, review_id):
        """Update a review"""
        review = self.model.query.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            setattr(review, key, value)

        self.add(review)
        return review
