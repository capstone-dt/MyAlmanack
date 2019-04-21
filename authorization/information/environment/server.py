import sys


# This checks whether the server is being run in a test environment.
# Code taken from: https://stackoverflow.com/a/4277798/8060864
def is_test_server(request):
    return len(sys.argv) > 1 and sys.argv[1] == "runserver"