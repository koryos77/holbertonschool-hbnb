#!/usr/bin/python3


class Review():
    """
    Review class to put review on a home.
    """
    def id():
        """
        string: Unique identifier for each review.
        """
        pass


    def text():
        """
        string: The content of the review. Required.
        """
        pass


    def rating():
        """
        integer: Rating given to the place, must be between 1 and 5.
        """
        pass


    def place():
        """
        place: Instance being reviewed. Must be validated to ensure the
        place exists.
        """
        pass


    def user():
        """
        user: Instance of who wrote the review. Must be validated to
        ensure the user exists.
        """
        pass


    def created_at():
        """
        DateTime: Timestamp when the review is created
        """
        pass


    def updated_at():
        """
        DateTime: Timestamp when the review is updated.
        """
        pass
