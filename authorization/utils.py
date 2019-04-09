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
            "%s is not a subclass of %s: %s" %
            (get_class_name(object), get_class_name(superclass), object)
        )