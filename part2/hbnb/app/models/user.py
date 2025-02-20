#!/usr/bin/python3


class User():
    """
    User class that defines the users.
    """
    def id():
        """
        string: Unique identifier for each user.
        """
        pass


    def first_name():
        """
        string: The first name of the user.
        Required, maximum length of 50 characters.
        """
        pass


    def last_name():
        """
        string: The last name of the user.
        Required, maximum length of 50 characters.
        """
        pass


    def email():
        """
        string: The email address of the user.
        Required, must be unique, and should follow standard email
        format validation.
        """
        pass


    def is_admin():
        """
        boolean: indicates whether the user has admin privileges.
        Defaults to False.
        """
        pass


    def created_at():
        """
        DateTime: Timestamp when the user is created.
        """
        pass


    def updated_at():
        """
        DateTime: Timestamp when the user is last updated.
        """
        pass
