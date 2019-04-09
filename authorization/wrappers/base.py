from ..utils import get_class_name, is_subclass, assert_subclass


class BaseWrapper:
    """
    The BaseWrapper object ...
    """
    
    def __init__(self, object):
        if hasattr(self, "_root"):
            # Make sure that the object is an instance of the root class.
            assert_subclass(object, self._root)
        elif hasattr(self, "wrap"):
            # Make sure that the is_wrappable() method has been overridden.
            if self.is_wrappable is BaseWrapper.is_wrappable:
                raise NotImplementedError(
                    "The is_wrappable() method has not been overridden to "
                    "complement the defined wrap() method in %s!" %
                    get_class_name(self)
                )
        else:
            # No valid wrapping method was set for the class.
            raise NotImplementedError(
                "There is no valid wrapping method set for %s! "
                "Either set the _root property or both the wrap() and "
                "is_wrappable() methods!" %
                get_class_name(self)
            )
        
        # Call the wrapping helper if it is defined. This can be used to extract
        #     information for the wrapper from the given object.
        if hasattr(self, "wrap"):
            self.wrap(object)
            
        
        # Set the object as the proxied object.
        self._object = object
    
    def __str__(self):
        return "%s[%s]" % (get_class_name(self), self._object)
    
    @classmethod
    def is_wrappable(cls, object):
        if hasattr(cls, "_root"):
            return is_subclass(object, cls._root)
        else:
            return False