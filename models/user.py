#!/usr/bin/python3
"""Declares the User class. Inherits from base model"""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a User

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    first_name = ""
    last_name = ""
    email = ""
    password = ""
