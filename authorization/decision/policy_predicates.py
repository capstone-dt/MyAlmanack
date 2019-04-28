from .policy import Policy
from ..utilities.reflection import assert_subclass

# Python
from enum import IntEnum


# The UnaryOperator enumeration class provides a set of available unary
#     operators for use with UnaryPolicyPredicate instances.
class UnaryOperator(IntEnum):
    NEGATE = 1


# The BinaryOperator enumeration class provides a set of available binary
#     operators for use with BinaryPolicyPredicate instances.
class BinaryOperator(IntEnum):
    AND = 1
    OR = 2
    XOR = 3


# The UnaryPolicyPredicate class allows for the construction of unary logical
#     predicates using Policy classes.
class UnaryPolicyPredicate(Policy):
    def __init__(self, operator, operand):
        assert_subclass(operator, UnaryOperator)
        self.operator = operator
        
        assert_subclass(operand, Policy)
        self.operand = operand
    
    def evaluate(self, *args, **kwargs):
        result = self.operand.evaluate(*args, **kwargs)
        
        if self.operator == UnaryOperator.NEGATE:
            # ~A
            return not result


# The BinaryPolicyPredicate class allows for the construction of binary logical
#     predicates using Policy classes.
class BinaryPolicyPredicate(Policy):
    def __init__(self, operator, operand1, operand2):
        assert_subclass(operator, BinaryOperator)
        self.operator = operator
        
        assert_subclass(operand1, Policy)
        self.operand1 = operand1
        
        assert_subclass(operand2, Policy)
        self.operand2 = operand2
    
    def evaluate(self, *args, **kwargs):
        operand1_result = self.operand1.evaluate(*args, **kwargs)
        
        if self.operator == BinaryOperator.AND:
            # A & B
            return operand1_result and self.operand2.evaluate(*args, **kwargs)
        elif self.operator == BinaryOperator.OR:
            # A | B
            return operand1_result or self.operand2.evaluate(*args, **kwargs)
        elif self.operator == BinaryOperator.XOR:
            # A ^ B
            return operand1_result != self.operand2.evaluate(*args, **kwargs)