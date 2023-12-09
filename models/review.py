#!/usr/bin/python3
"""Defines the Review class. Inherits from base model"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review.

    Attributes:
        text (str): The text of the review
        user_id (str): The User id
        place_id (str): The Place id
    """

    text = ""
    user_id = ""
    place_id = ""
