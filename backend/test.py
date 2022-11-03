import base64
import os


def a_test(a, b):
    return str(a) + str(b)


print(base64.b64encode(os.urandom(48)))


