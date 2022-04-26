def a_test(a, b):
    return str(a) + str(b)


print(list(map(a_test, [1, 2], [2])))
