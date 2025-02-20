#!/usr/bin/python3


class Place():
    """
    Place class, to add a place or to modify one
    """
    def id():
        """
        string: Unique identifier for each place.
        """
        pass


    def title():
        """
        string: The title of the place. Required, maximum length of
        100 characters.
        """
        pass


    def description():
        """
        string: Detailed description of the place.
        """
        pass


    def price():
        """
        float: The per night for the place. Must be a positive value.
        """
        pass


    def latitude():
        """
        float: Latitude coordinate for the place location.
        Must be within the range of -90.0 to 90.0.
        """
        pass


    def longitude():
        """
        float: Longitude coordinates for the place location.
        Must be within the range of -180.0 to 180.0
        """
        pass


    def owner():
        """
        user: Instance of who owns the place: This should be validated to
        ensure the owner exists.
        """
        pass


    def created_at():
        """
        DateTime: Timestamp when the place is created.
        """
        pass


    def updated_at():
        """
        DateTime: Timestamp when the place is last updated.
        """
        pass
