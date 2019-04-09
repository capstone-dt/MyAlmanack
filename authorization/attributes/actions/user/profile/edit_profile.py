from authorization.attributes.actions.user import BinaryUserHttpAction
from authorization import policies


class EditProfile(BinaryUserHttpAction):
    policies = [
        # A user can only edit himself/herself.
        policies.miscellaneous.SubjectIsResource
    ]