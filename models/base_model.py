#!/usr/bin/python3
"""Defines the BaseModel class."""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """Represents the Base Model of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initializes a new BaseModel.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        timeformat = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, timeformat)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    
    
    def __str__(self):
        """Return the print/string representation of the BaseModel instance."""
        className = self.__class__.__name__
        return "[{}] ({}) {}".format(className, self.id, self.__dict__)

    def to_dict(self):
        """Returns the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object
        """
        newdict = self.__dict__.copy()
        newdict["__class__"] = self.__class__.__name__
        newdict["updated_at"] = self.updated_at.isoformat()
        newdict["created_at"] = self.created_at.isoformat()
        return newdict

    def save(self):
        """Updates updated_at with the current datetimeand saves"""
        self.updated_at = datetime.today()
        models.storage.save()
