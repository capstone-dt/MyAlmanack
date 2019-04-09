from .base import BaseWrapper


class User(BaseWrapper):
    def wrap(self, object):
        self.hi = 1
    
    @classmethod
    def is_wrappable(cls, object):
        return True