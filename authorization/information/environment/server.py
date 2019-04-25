import sys


# This helps determine whether the server is running in a test environment.
# Code taken from: https://stackoverflow.com/a/4277798/8060864
in_test_environment = len(sys.argv) > 1 and sys.argv[1] == "runserver"