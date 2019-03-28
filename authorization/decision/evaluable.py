class EvaluableMetaclass(type):
    def __new__(cls, name, bases, kwargs):
        _class = super().__new__(cls, name, bases, kwargs)
        
        # Make all subclass instances inherit the magic methods as well.
        _class.__invert__ = cls.__invert__
        _class.__and__ = cls.__and__
        _class.__or__ = cls.__or__
        _class.__xor__ = cls.__xor__
        
        return _class
    
    # ~ operator
    def __invert__(self):
        from .policy_predicates import UnaryPolicyPredicate, UnaryOperator
        return UnaryPolicyPredicate(UnaryOperator.NEGATE, self)
    
    # & operator
    def __and__(self, other):
        from .policy_predicates import BinaryPolicyPredicate, BinaryOperator
        return BinaryPolicyPredicate(BinaryOperator.AND, self, other)
    
    # | operator
    def __or__(self, other):
        from .policy_predicates import BinaryPolicyPredicate, BinaryOperator
        return BinaryPolicyPredicate(BinaryOperator.OR, self, other)
    
    # ^ operator
    def __xor__(self, other):
        from .policy_predicates import BinaryPolicyPredicate, BinaryOperator
        return BinaryPolicyPredicate(BinaryOperator.XOR, self, other)


class Evaluable(metaclass=EvaluableMetaclass):
    @classmethod
    def evaluate(cls, *args, **kwargs):
        raise NotImplementedError(
            "The evaluate() method of %s has not been implemented!" %
            cls.__name__
        )