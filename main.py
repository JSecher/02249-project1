import string
from itertools import chain

SIGMA = set(string.ascii_lowercase)
GAMMA = set(string.ascii_uppercase)


def superstringwithexpansion():
    inputs = decoder()

    if check_and_clean_inputs(inputs):
        s, t, r = inputs
        print(s)
        for element in t:
            print(element)
        for element in r:
            print(f"{element}: {r[element]}")

        for t_string in t:
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


def check_and_clean_inputs(inputs):
    s, t, r = inputs

    well_formed = check_superstring(s) \
        and check_and_clean_subsets(s, r) \
        and check_and_clean_strings(s, t, r)

    return well_formed


def check_superstring(s):
    return not contains_letter_outside_alphabets(s, SIGMA)


def check_and_clean_subsets(s, r):
    for gamma in r:
        if gamma not in GAMMA:
            return False

        for expansion in reversed(r[gamma]):
            if contains_letter_outside_alphabets(expansion, SIGMA):
                return False

            if expansion not in s:
                r[gamma].remove(expansion)

    return True


def check_and_clean_strings(s, t, r):
    for t_string in t:
        contains_letter_from_gamma = False

        for letter in t_string:
            if letter in GAMMA:
                contains_letter_from_gamma = True
                if not r[letter]:
                    return False
            else:
                if letter not in SIGMA:
                    return False

        if not contains_letter_from_gamma and t_string not in s:
            return False

    t.sort(key=elements_from_GAMMA)

    return True


def elements_from_GAMMA(word):
    return len([letter for letter in word if letter in GAMMA])


def contains_letter_outside_alphabets(word, alphabet):
    for letter in word:
        if letter not in alphabet:
            return True

    return False


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
            print(f"{res}:{result[res][0]}")
