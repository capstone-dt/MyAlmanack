from authorization.attributes.actions.user import BinaryUserAction
from authorization import policies


class EditProfile(BinaryUserAction):
    policies = [
        # A user can edit his or her own profile.
        policies.miscellaneous.SubjectIsResource
    ]