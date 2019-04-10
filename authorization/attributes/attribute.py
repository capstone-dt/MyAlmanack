from ..utilities.wrapper import Wrapper
from ..utilities.reflection import get_class_name, is_subclass

# Python
from importlib import import_module
from inspect import isclass, getmembers
from os import listdir


class Attribute(Wrapper):
    pass


def wrap_attribute(attribute_class, object, wrappers_directory):
    # Define a function for picking classes out of wrapper modules.
    checker = lambda member: (
        isclass(member) and is_subclass(member, attribute_class)
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
        for (_, _class) in getmembers(wrapper_module, checker):
            if is_subclass(object, _class):
                return object
            elif _class.is_wrappable(object):
                return _class(object)
    
    # If we get to this point, then there was no wrapper class available for the
    #     given object.
    raise ValueError(
        "There is no %s wrapper class available for %s!" %
        (get_class_name(attribute_class), get_class_name(object))
    )