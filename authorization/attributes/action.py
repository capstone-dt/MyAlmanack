from ..utilities.reflection import assert_subclass


# The Action class is used to bind specific authorization attributes and
#     policies to specific actions in a way that would make sense.
# For example, the action to view a user's profile might require the following
#     constraints:
#   * Subject: User 1
#   * Resource: User 2's profile
#   * Policies: User 1 must be a friend with user 2.
class Action:
    # This asserts that the attribute class constraints bound before runtime
    #     have been satisfied.
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