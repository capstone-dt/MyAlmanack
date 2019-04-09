from authorization.attributes.actions.user import BinaryUserAction
from authorization import policies


class EditProfile(BinaryUserAction):
    policies = [
        # A user can only edit himself/herself.
        policies.miscellaneous.SubjectIsResource
    ]