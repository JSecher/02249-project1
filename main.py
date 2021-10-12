
def read_input():
    raise NotImplementedError


def decoder():
    raise NotImplementedError


def superstringwithexpansion():
    raise NotImplementedError


if __name__ == '__main__':

    result = superstringwithexpansion()

    if result == "No":
        print("No")
    else:
        for res in result:
            print(f"{res[0]}:{res[1]}")
