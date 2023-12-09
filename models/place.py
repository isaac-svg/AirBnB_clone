#!/usr/bin/python3
"""Defines the Place class. Inherits from base model"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represents a place.

    Attributes:
        name (str): The name of the place.
        amenity_ids (list): A list of Amenity ids.
        description (str): The description of the place.
        number_rooms (int): The number of rooms of the place.
        number_bathrooms (int): The number of bathrooms of the place.
        max_guest (int): The maximum number of guests of the place.
        city_id (str): The City id.
        longitude (float): The longitude of the place.
        price_by_night (int): The price by night of the place.
        user_id (str): The User id.
        latitude (float): The latitude of the place.
    """

    description = ""
    city_id = ""
    name = ""
    user_id = ""
    amenity_ids = []
    number_bathrooms = 0
    number_rooms = 0
    longitude = 0.0
    latitude = 0.0
    price_by_night = 0
    max_guest = 0
