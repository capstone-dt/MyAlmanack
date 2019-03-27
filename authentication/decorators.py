def login_notrequired(view_function):
    setattr(view_function, "_authentication_login_notrequired", True)
    return view_function