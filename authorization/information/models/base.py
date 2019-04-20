from authorization.utilities.wrapper import Wrapper


class ModelWrapper(Wrapper):
    """
    Model Wrapper
    ============
    The model wrapper class encapsulates the database models to isolate any
        unexpected changes.
    """
    
    def __eq__(self, other):
        return isinstance(other, ModelWrapper) and self.uid == other.uid
    
    def __hash__(self):
        return hash(self.uid)