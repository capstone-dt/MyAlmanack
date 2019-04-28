from inspect import isclass


# This returns the immediate ancestor class of an object.
def get_class_of(object):
    return object if isclass(object) else object.__class__


# This returns the name of the class of an object.
def get_class_name(object):
    _class = get_class_of(object)
    return getattr(_class, "__name__", str(_class))


# This checks whether an object is a subclass of a given superclass.
def is_subclass(object, superclass):
    return object != superclass and issubclass(get_class_of(object), superclass)


# This asserts that an object is a subclass of a given superclass, and raises
#     an error if the assertion fails.
def assert_subclass(object, superclass):
    if not is_subclass(object, superclass):
        raise ValueError(
            "A subclass of %s was expected, but %s was given: %s" %
            (get_class_name(superclass), get_class_name(object), object)
        )