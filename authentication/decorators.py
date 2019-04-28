# This marks a Django view as not requiring authentication so the Firebase
#     session middleware would not redirect the user to the login screen.
def login_notrequired(view_function):
    setattr(view_function, "_authentication_login_notrequired", True)
    return view_function