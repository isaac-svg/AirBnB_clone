#!/usr/bin/python3
"""Defines the FileStorage class"""
import json
from models.amenity import Amenity
from models.state import State
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City
from models.base_model import BaseModel


class FileStorage:
    """Represents a storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """Serializes from (object to string)  __objects to the JSON file __file_path."""
        old_dict = FileStorage.__objects
        newdict = {obj: old_dict[obj].to_dict() for obj in old_dict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(newdict, f)

    def reload(self):
        """Deserializes (from string to object) the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
