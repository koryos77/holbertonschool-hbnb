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
        review = self.get(review_id)
        if not review:
            return None
        review.update(review_data)
        return review
