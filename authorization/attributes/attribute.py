from ..utils import get_class_name, is_subclass, assert_subclass

# Python
from importlib import import_module
import inspect
from os import listdir


class Attribute:
    _root = None
    
    def __init__(self, object):
        # Make sure that the subclass extending this class has set the root.
        if self._root is None:
            raise ValueError("The \"_root\" class property has not been set!")
        
        # Make sure that the object is a subclass instance of the root class.
        assert_subclass(object, self._root)
        
        # Set the object as the proxied object.
        self._object = object
    
    def __str__(self):
        return "%s[%s]" % (get_class_name(self), self._object)


def wrap_attribute(attribute_class, object, wrappers_directory):
    # Define a function for picking classes out of wrapper modules.
    checker = lambda member: (
        inspect.isclass(member) and is_subclass(member, attribute_class)
    )
    
    # List all the modules in the given wrappers directory.
    files = listdir("authorization/attributes/" + wrappers_directory)
    for file in filter(lambda file: file.endswith(".py"), files):
        # Dynamically import the wrapper module.
        wrapper_module = import_module(
            ".%s.%s" % (wrappers_directory, file.rstrip(".py")),
            "authorization.attributes"
        )
        
        # Find the corresponding wrapper class in the wrapper module.
        for (_, _class) in inspect.getmembers(wrapper_module, checker):
            if is_subclass(object, _class):
                return object
            elif isinstance(object, _class._root):
                return _class(object)
    
    # If we get to this point, then there was no wrapper class available for
    # the given object.
    raise ValueError(
        "There is no %s wrapper class available for %s!" %
        (get_class_name(attribute_class), get_class_name(object))
    )