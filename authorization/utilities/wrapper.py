from .reflection import get_class_name, is_subclass, assert_subclass


# The Wrapper class provides a way to wrap or proxy objects.
# For an example implementation, see information.models.base.ModelWrapper.
class Wrapper:
    def __init__(self, object):
        if hasattr(self, "wrap"):
            # Make sure that the is_wrappable() method has been overridden.
            if self.is_wrappable is Wrapper.is_wrappable:
                raise NotImplementedError(
                    "The is_wrappable() method has not been overridden to "
                    "complement the defined wrap() method in %s!" %
                    get_class_name(self)
                )
            
            # Make sure this class can wrap the given object.
            if not self.is_wrappable(object):
                raise ValueError(
                    "%s is not wrappable with %s!" %
                    (get_class_name(object), get_class_name(self))
                )
        elif hasattr(self, "_root"):
            # Make sure that the object is an instance of the root class.
            assert_subclass(object, self._root)
        else:
            # No valid wrapping method was set for the class.
            raise NotImplementedError(
                "There is no valid wrapping method set for %s! "
                "Either set the _root property, or both the wrap() and "
                "is_wrappable() methods!" %
                get_class_name(self)
            )
        
        # Call the wrapping helper if it is defined. This can be used to extract
        #     information for the wrapper from the given object.
        self._object = self.wrap(object) if hasattr(self, "wrap") else object
    
    # This checks whether a given object is wrappable with this wrapper class.
    # This is to be overridden if a wrap() method is also defined.
    @classmethod
    def is_wrappable(cls, object):
        if hasattr(cls, "_root"):
            return is_subclass(object, cls._root)
        else:
            return False
    
    # This simply provides a default prettified printing of Wrapper instances.
    def __str__(self):
        return "Wrapper<%s>[%s]" % (get_class_name(self), self._object)