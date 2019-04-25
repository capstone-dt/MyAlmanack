from ..utilities.reflection import assert_subclass


class Action:
    @classmethod
    def assert_attribute_classes(cls, subject, resource, context):
        # Assert the subject attribute's class if available.
        if hasattr(cls, "_subject_class"):
            assert_subclass(subject, cls._subject_class)
        
        # Assert the resource attribute's class if available.
        if hasattr(cls, "_resource_class"):
            assert_subclass(resource, cls._resource_class)
        
        # Assert the context attribute's class if available.
        if hasattr(cls, "_context_class"):
            assert_subclass(context, cls._context_class)