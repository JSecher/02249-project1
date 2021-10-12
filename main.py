import re


def decoder():
    """
    Reads inputs from stdin

    Returns:
        s : str : Superstring to check against
        t : list : List of t strings to compute expansions of
        r : dict : Dictionary of possible expansions
    """
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


def checkSuperString(s):
    for c in s:
        if not c in string.ascii_lowercase
            
    return True


def checkStrings(s, t):
    return True


def checkSubsets(s, r):
    return True


def checkInputs(inputs):
    s, t, r = inputs

    wellformed = checkSuperString(s) and \
                 checkStrings(s, t) and \
                 checkSubsets(s, r)

    return wellformed


def superstringwithexpansion():
    inputs = decoder()
    if checkInputs(inputs):
        s, t, r = inputs
    else:
        return "NO"

    return "YES"


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