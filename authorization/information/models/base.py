from authorization.utilities.wrapper import Wrapper
from authorization.utilities.reflection import get_class_name


# The ModelWrapper class' metaclass simply ensures that subclasses of
#     ModelWrapper will receive their own instance cache instead of using
#     a single master cache in the base ModelWrapper class.
class ModelWrapperMetaclass(type):
    def __new__(cls, name, bases, keywords):
        # This is just boilerplate Python stuff for metaclass creation.
        _class = super().__new__(cls, name, bases, keywords)
        
        # Create a cache specific to the extending model wrapper class.
        _class._cache = {}
        
        return _class


# The ModelWrapper class encapsulates the database models in an attempt to
#     isolate any unexpected changes in those models to a single location.
# It also adds the ability to define a consistent usage of database models
#     within the subsystem.
class ModelWrapper(Wrapper, metaclass=ModelWrapperMetaclass):
    # This overrides the behavior of wrapper object instantiation to allow
    #     for instance caching.
    def __new__(cls, object):
        try:
            # Use the cached instance if possible.
            if object not in cls._cache:
                cls._cache[object] = super().__new__(cls)
            
            # For some unknown reason, str() must be called on the instance for
            #     everything to work properly.
            # This was determined when everything suddenly began to work
            #     properly after I tried to print out the cached object.
            # This might be due to some weird initialization procedure that I am
            #     unaware of (maybe Django's lazy model loading?).
            # Do NOT remove the str() call.
            str(cls._cache[object])
            return cls._cache[object]
        except:
            # Caching is not possible. Simply create and return a new instance.
            return super().__new__(cls)
    
    # This returns the UID of this wrapper instance.
    @property
    def uid(self):
        raise NotImplementedError(
            "The uid field has not been implemented for %s!" %
            get_class_name(self)
        )
    
    # This returns a wrapper instance in the database given their UID.
    @classmethod
    def from_uid(cls, uid):
        raise NotImplementedError(
            "The from_uid() method has not been implemented for %s!" %
            get_class_name(cls)
        )
    
    # This returns a set of wrapper instances in the database given their UIDs.
    @classmethod
    def from_uids(cls, uids):
        return frozenset(cls.from_uid(uid) for uid in uids)
    
    # This overrides the behavior of the equality operator.
    def __eq__(self, other):
        return isinstance(other, ModelWrapper) and self.uid == other.uid
    
    # This implements the hashing of a ModelWrapper object for use with
    #     collection objects such as dicts and sets.
    def __hash__(self):
        return hash(self.uid)