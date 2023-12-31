#!/usr/bin/python3
"""Declares the HBNB console"""
import re
from models.state import State
from shlex import split
from models.review import Review
from models.base_model import BaseModel
from models.amenity import Amenity
from models import storage
from models.user import User
import cmd
from models.city import City
from models.place import Place


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [j.strip(",") for j in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Declares the HBNB cmd interpreter

    Attributes:
        prompt (str): The cmd prompt
    """

    prompt = "(hbnb) "
    __classes = {
        "Review"
        "City",
        "User",
        "Amenity",
        "Place",
        "State",
        "BaseModel",
    }

    

    def default(self, arg):
        """Default behavior for cmd module when input is invalid or not correct"""
        argdict = {
            "update": self.do_update,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "all": self.do_all,
            "show": self.do_show
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False
    
    def emptyline(self):
        """ignore an empty line"""
        pass

    def do_quit(self, arg):
        """Exit the program"""
        return True

    def do_EOF(self, arg):
        """End of file (EOF) signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id
        """
        argl = parse(arg) #argument length
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    
    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance with a given id."""
        argl = parse(arg)
        objdict = storage.all() #get all stored data
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance with a given id
        """
        argl = parse(arg)
        objdict = storage.all() #get all stored data
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Prints string representations of all instances of a given class
        If no class is specified, prints all instantiated objects
        """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    
    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arguments = parse(arg)
        objdict = storage.all() #get all objects from storage

        if len(arguments) == 0:
            print("** class name missing **")
            return False
        if arguments[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arguments) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arguments[0], arguments[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(arguments) == 2:
            print("** attribute name missing **")
            return False
        if len(arguments) == 3:
            try:
                type(eval(arguments[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arguments) == 4:
            obj = objdict["{}.{}".format(arguments[0], arguments[1])]
            if arguments[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arguments[2]])
                obj.__dict__[arguments[2]] = valtype(arguments[3])
            else:
                obj.__dict__[arguments[2]] = arguments[3]
        elif type(eval(arguments[2])) == dict:
            obj = objdict["{}.{}".format(arguments[0], arguments[1])]
            for k, v in eval(arguments[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Get the number of instances of a given class."""
        arguments = parse(arg)
        count = 0
        for obj in storage.all().values():
            if arguments[0] == obj.__class__.__name__:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
