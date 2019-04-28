# The Evaluable class' metaclass allows for unary and binary predicate
#     constructions directly on subclasses of Evaluable. Their evaluation order
#     depends on Python's operator precedence.
# For example, given Evaluable classes A and B:
#   * ~A (not)
#   * A & B (and)
#   * A | B (or)
#   * A ^ B (xor)
#   * ~(~A | B) & A (any logical predicate expression will work)
class EvaluableMetaclass(type):
    def __new__(cls, name, bases, keywords):
        # This is just boilerplate Python stuff for metaclass creation.
        _class = super().__new__(cls, name, bases, keywords)
        
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


# The Evaluable class provides a way to build and evaluate logical predicate
#     expressions using subclasses and their instances, and evaluating them
#     through their implemented evaluate() method.
class Evaluable(metaclass=EvaluableMetaclass):
    pass