import string
from itertools import chain

SIGMA = set(string.ascii_lowercase)
GAMMA = set(string.ascii_uppercase)


def superstringwithexpansion():
    inputs = decoder()
    if check_inputs(inputs) and clean_inputs(inputs):
        s, t, r = inputs

        for t_string in sorted(t):
            if len(t_string) > 1:
                r_pruned = naive_solver(s, [t_string], r)
                for key, item in r_pruned.items():
                    if len(item) == 0:
                        return None
                    r[key] = item

        r_final = naive_solver(s, t, r)
        for _, item in r_final.items():
            if len(item) == 0:
                return None
        return r_final

    else:
        return None


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


def check_inputs(inputs):
    s, t, r = inputs

    well_formed = check_superString(s) \
                  and check_subsets(r) \
                  and check_strings(t, r)

    return well_formed


def check_superString(s):
    return not contains_letter_outside_alphabets(s, SIGMA)


def check_subsets(r):
    for gamma in r:
        if gamma not in GAMMA:
            return False

        for expansion in r[gamma]:
            if contains_letter_outside_alphabets(expansion, SIGMA):
                return False

    return True


def check_strings(t, r):
    all_letter = set().union(*(SIGMA, r.keys()))
    for t_string in t:
        if contains_letter_outside_alphabets(t_string, all_letter):
            return False

    return True


def contains_letter_outside_alphabets(word, alphabet):
    for letter in word:
        if letter not in alphabet:
            return True

    return False


def clean_inputs(inputs):
    s, t, r = inputs
    r = remove_impossible_expansions(s, t, r)

    # Check if there is an impossible mapping i.e. empty list in r
    if [] in r.values():
        return None
    else:
        return s and t and r


def remove_impossible_expansions(s, t, r):
    r = remove_expansions_not_in_s(s, r)
    # r = remove_expansions_incompatible_with_t(s, t, r)
    return r


def remove_expansions_not_in_s(s, r):
    for gamma in r:
        r[gamma] = [expansion for expansion in r[gamma] if expansion in s]

    return r


def remove_expansions_incompatible_with_t(s, t, r):
    for gamma in r:
        pass
    pass


def naive_solver(s, t, r):
    gammas = list({letter for letter in chain(*t) if letter in GAMMA})
    accepted_expansions = {g: set() for g in gammas}
    for expansion in all_possible_expansions(gammas, r):
        for word in t:
            copy = word
            for i in range(len(gammas)):
                copy = copy.replace(gammas[i], expansion[i])
            if copy not in s:
                break
        else:
            for i, g in enumerate(gammas):
                accepted_expansions[g].add(expansion[i])
            # return {gammas[i]: expansion[i] for i in range(len(gammas))}
    for key, item in accepted_expansions.items():
        accepted_expansions[key] = list(item)
    return accepted_expansions


def all_possible_expansions(letters, expansions):
    n = len(letters)
    possible_values = [len(expansions[letter]) for letter in letters]
    indices = [0] * n

    yield [expansions[letters[j]][indices[j]] for j in range(n)]
    while n:
        for i in reversed(range(n)):
            indices[i] += 1
            if indices[i] >= possible_values[i]:
                indices[i] = 0
            else:
                yield [expansions[letters[j]][indices[j]] for j in range(n)]
                break
        else:
            return


if __name__ == '__main__':
    result = superstringwithexpansion()
    if not result:
        print("NO")
    else:
        for res in sorted(result):
            print(f"{res}:{result[res]}")
