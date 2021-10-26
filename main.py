import string
from itertools import chain

SIGMA = set(string.ascii_lowercase)
GAMMA = set(string.ascii_uppercase)


def superstring_with_expansion():
    raw_input = decoder()
    if raw_input is None:
        return None

    _, _, R_raw = raw_input
    cleansed_input = clean_input(raw_input)
    if cleansed_input is None:
        return None

    s, T, R = cleansed_input
    if not T or not R:  # The problem is trivially solved
        return R_raw

    R_pruned = prune_expansions(s, T, R)
    if R_pruned is None:
        return None

    R_final = naive_solver_final(s, T, R_pruned)
    if not R_final:
        return None

    result = dict()
    for gamma in R_raw:
        if gamma in R_final:
            result[gamma] = R_final[gamma]
        else:
            result[gamma] = R_raw[gamma][0]

    return result


def decoder():
    raw_input = read_input()
    if not verify_input(raw_input):
        return None

    return raw_input


def read_input():
    k = int(input())
    s = str(input()).strip()
    T = read_strings(k)
    R = read_subsets()

    return s, T, R


def read_strings(k):
    T = set()
    for _ in range(k):
        T.add(str(input()).strip())

    return list(T)


def read_subsets():
    R = dict()
    while True:
        try:
            input_string = str(input())
            gamma = input_string[0]
            expansions = {item.strip() for item in input_string[2:].split(",")}
            R[gamma] = list(expansions)
        except EOFError:
            break

    return R


def verify_input(raw_input):
    s, T, R = raw_input

    well_formed = check_superString(s) \
        and check_subsets(R) \
        and check_strings(T, R)

    return well_formed


def check_superString(s):
    return not contains_letter_outside_alphabet(s, SIGMA)


def check_subsets(R):
    for gamma in R:
        if gamma not in GAMMA:
            return False

        for expansion in R[gamma]:
            if not expansion or contains_letter_outside_alphabet(expansion, SIGMA):
                return False

    return True


def check_strings(T, R):
    alphabet = set().union(SIGMA, R.keys())
    for t in T:
        if contains_letter_outside_alphabet(t, alphabet):
            return False

    return True


def contains_letter_outside_alphabet(word, alphabet):
    for letter in word:
        if letter not in alphabet:
            return True

    return False


def clean_input(raw_input):
    s, T, R = raw_input
    T_cleansed = remove_duplicates_and_valid_strings(s, T)
    if T_cleansed is None:
        return None

    R_cleansed = remove_superfluous_subsets_and_expansions(s, T_cleansed, R)
    if R_cleansed is None:
        return None

    return s, T_cleansed, R_cleansed


def remove_duplicates_and_valid_strings(s, T):
    T_cleansed = set()
    for t in T:
        if t not in T_cleansed:
            if contains_letter_outside_alphabet(t, SIGMA):
                T_cleansed.add(t)
            else:
                if t not in s:
                    return None
    T_sorted = sorted(list(T_cleansed), key=number_of_letters_from_GAMMA)
    return T_sorted


def number_of_letters_from_GAMMA(word):
    return len([letter for letter in word if letter in GAMMA])


def remove_superfluous_subsets_and_expansions(s, T, R):
    R_cleansed = dict()
    used_gammas = {letter for letter in chain(*T) if letter in GAMMA}
    for gamma in used_gammas:
        valid_expansions = [expansion for expansion in R[gamma] if expansion and expansion in s]
        if not valid_expansions:
            return None
        else:
            R_cleansed[gamma] = valid_expansions

    return R_cleansed


def prune_expansions(s, T, R):
    R_pruned = R.copy()
    for t in T:
        valid_expansions = naive_solver(s, [t], R_pruned)
        if not valid_expansions:
            return None

        for key, value in valid_expansions.items():
            if not value:
                return None
            R_pruned[key] = value

    return R_pruned


def naive_solver(s, T, R):
    gammas = list({letter for letter in chain(*T) if letter in GAMMA})
    accepted_expansions = {g: set() for g in gammas}
    for expansion in all_possible_expansions(gammas, R):
        for t in T:
            copy = t
            for i in range(len(gammas)):
                copy = copy.replace(gammas[i], expansion[i])
            if copy not in s:
                break
        else:
            for i, g in enumerate(gammas):
                accepted_expansions[g].add(expansion[i])

    for key, item in accepted_expansions.items():
        accepted_expansions[key] = list(item)
    return accepted_expansions


def naive_solver_final(s, T, R):
    gammas = list({letter for letter in chain(*T) if letter in GAMMA})
    for expansion in all_possible_expansions(gammas, R):
        for t in T:
            copy = t
            for i in range(len(gammas)):
                copy = copy.replace(gammas[i], expansion[i])
            if copy not in s:
                break
        else:
            return {gammas[i]: expansion[i] for i in range(len(gammas))}

    return None


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
    output = superstring_with_expansion()
    if not output:
        print("NO")
    else:
        for r in sorted(output):
            print(f"{r}:{output[r]}")