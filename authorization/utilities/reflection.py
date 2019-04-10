from inspect import isclass


def get_class_of(object):
    return object if isclass(object) else object.__class__


def get_class_name(object):
    _class = get_class_of(object)
    return getattr(_class, "__name__", str(_class))


def is_subclass(object, superclass):
    return object != superclass and issubclass(get_class_of(object), superclass)


def assert_subclass(object, superclass):
    if not is_subclass(object, superclass):
        raise ValueError(
            "A subclass of %s was expected, but %s was given: %s" %
            (get_class_name(superclass), get_class_name(object), object)
        )