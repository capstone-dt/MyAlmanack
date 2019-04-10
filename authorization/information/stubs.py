class ContactList:
    def __init__(self, uids):
        self.contact_names = uids


class Profile:
    def __init__(self, firebase_id):
        self.firebase_id = firebase_id
        self.contact_list = ContactList([
            #firebase_id
        ])


class Group:
    def __init__(self, group_name):
        self.group_name = group_name
        self.group_members = [
            User.from_uid("SJ9F2PEcMNWWDqQWzgsdvuRK8Rg2")
        ]