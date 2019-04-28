from ..utilities.wrapper import Wrapper
from ..utilities.reflection import get_class_name, is_subclass

# Python
from importlib import import_module
from inspect import isclass, getmembers
from os import listdir


# The Attribute class simply provides an interface for AuthorizationRequest's
#     attributes by wrapping specific classes of objects passed in by the
#     subsystem's API users.
class Attribute(Wrapper):
    pass


# This attempts to wrap a given object using the correct wrapper class of the
#     given attribute class located in the provided directory.
# It is used to simplify passing in attributes for the AuthorizationRequest
#     class so that users of the subsystem's APIs won't have to manually wrap
#     them.
def wrap_attribute(attribute_class, object, wrappers_directory):
    # Define a function for picking classes out of wrapper modules.
    picker = lambda member: (
        isclass(member) and is_subclass(member, attribute_class)
    )
    
    # List all the modules in the given wrappers directory.
    files = listdir("authorization/attributes/" + wrappers_directory)
    for file in filter(lambda file: file.endswith(".py"), files):
        # Dynamically import the wrapper module.
        wrapper_module = import_module(
            ".%s.%s" % (wrappers_directory, file.rsplit(".py", 1)[0]),
            "authorization.attributes"
        )
        
        # Find the corresponding wrapper class in the wrapper module.
        for (_, _class) in getmembers(wrapper_module, picker):
            if isinstance(object, _class):
                # If the given object is already an instance of the current
                #     attribute class, then just return it.
                return object
            elif _class.is_wrappable(object):
                # If the given object is wrappable using the current attribute
                #     class, then wrap it.
                return _class(object)
    
    # If we get to this point, then there was no wrapper class available for the
    #     given object.
    raise ValueError(
        "There is no %s wrapper class available for %s!" %
        (get_class_name(attribute_class), get_class_name(object))
    )