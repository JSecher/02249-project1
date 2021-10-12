import re


def decoder():
    n = int(input())
    s = str(input())
    t = []  # list for all t strings
    r = dict()  # dict for all R sets
    for _ in range(n):
        t.append(str(input()))
    while True:
        try:
            ri = str(input())
            gamma = ri[0]
            expansions = ri[2:].split(",")
            r[gamma] = expansions
        except EOFError:
            break

    return s, t, r


def superstringwithexpansion():
    inputs = decoder()
    if inputs:
        s, t, r = inputs
    else:
        return "NO"
    

if __name__ == '__main__':

    result = superstringwithexpansion()

    print(result)
    """
    if result == "NO":
        print(result)
    else:
        for res in result:
            print(f"{res[0]}:{res[1]}")
    """