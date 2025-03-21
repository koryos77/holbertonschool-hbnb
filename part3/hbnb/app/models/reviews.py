from .base_model import BaseModel
from app.extensions import db
from .places import Place
from .user import User

class Review(BaseModel):
	__tablename__ = 'reviews'
	__table_args__ = {'extend_existing': True} 

	id = db.Column(db.Integer, nullable=False, primary_key=True)
	text = db.Column(db.String(500), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
	user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

	def __init__(self, text, rating, place, user):
		super().__init__()
		self.text = text
		self.rating = rating
		self.place = place
		self.user = user
	
	@property
	def text(self):
		return self.__text
	
	@text.setter
	def text(self, value):
		if not value:
			raise ValueError("Text cannot be empty")
		if not isinstance(value, str):
			raise TypeError("Text must be a string")
		self.__text = value

	@property
	def rating(self):
		return self.__rating
	
	@rating.setter
	def rating(self, value):
		if not isinstance(value, int):
			raise TypeError("Rating must be an integer")
		super().is_between('Rating', value, 1, 6)
		self.__rating = value

	@property
	def place(self):
		return self.__place
	
	@place.setter
	def place(self, value):
		if not isinstance(value, Place):
			raise TypeError("Place must be a place instance")
		self.__place = value

	@property
	def user(self):
		return self.__user
	
	@user.setter
	def user(self, value):
		if not isinstance(value, User):
			raise TypeError("User must be a user instance")
		self.__user = value

	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'rating': self.rating,
			'place_id': self.place.id,
			'user_id': self.user.id
		}
