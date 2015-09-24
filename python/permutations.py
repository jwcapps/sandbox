
"""
Permutations to and fro Lehmer Codes and indexes

All permutations are of the form 0 to n-1

https://en.wikipedia.org/wiki/Lehmer_code#Encoding_and_decoding
https://en.wikipedia.org/wiki/Factorial_number_system
"""

import itertools

def permutation_to_lehmer(permutation):
    # for each element subtract the number of elements to the left that are smaller
    return [v - sum(1 for j in range(i) if permutation[j] < v)
            for i, v in enumerate(permutation)]

def lehmer_to_permutation(lehmer):
    perm = list(lehmer)
    n = len(perm)
    
    # from right to left inc elements to the right of each element that are >=
    for i in reversed(range(n)):
        for j in range(i+1, n):
            if perm[j] >= perm[i]:
                perm[j] += 1
    return perm

def lehmer_to_int(lehmer):
    index = 0
    base = 1
    # lehmer is a list of the coefficients in the factoradic base
    for i, v in enumerate(reversed(lehmer), start=1):
        index += v*base
        base *= i
    return index

def permutation_index(permutation):
    return lehmer_to_int(permutation_to_lehmer(permutation))

def int_to_lehmer(n, size=0):
    lehmer = []

    # divide n by successive factoradic base and collect remainders
    for base in itertools.count(start=1):
        lehmer.append(n % base)

        n //= base
        if not n:
            break

    # resultant lehmer list may be smaller than required size so pad
    lehmer += [0] * (size - len(lehmer))
    lehmer = reversed(lehmer)
    return lehmer

def nth_permutation(n, size=0):
    """nth permutation of 0..size-1

    where n is from 0 to size! - 1
    """
    
    lehmer = int_to_lehmer(n, size)
    return lehmer_to_permutation(lehmer)

def nth_permutation_from_elements(n, elements):
    """arrange the list of elements into the nth permutation

    where n is from 0 to len(elements)! - 1
    elements must be complete including any required duplicates and sorted
    in ascending lexographic order

    nth_permutation_from_elements(2, [0,1,1,2,3,5]) -> [0,1,1,3,2,5]
    """

    lehmer = int_to_lehmer(n, len(elements))
    elements = list(elements)
    # lehmer is a list of indexes assuming the item is removed each time
    return [elements.pop(i) for i in lehmer]


assert all(permutation_to_lehmer(perm) == factoradic
           for perm, factoradic in zip(itertools.permutations(range(5)),
                                       ([a,b,c,d,e]
                                        for a in range(5)
                                        for b in range(4)
                                        for c in range(3)
                                        for d in range(2)
                                        for e in range(1))))

assert all(lehmer_to_permutation(permutation_to_lehmer(perm)) == list(perm)
           for perm in itertools.permutations(range(5)))

assert all(permutation_index(perm) == i
           for i, perm in enumerate(itertools.permutations(range(5))))

assert all(nth_permutation(n, 5) == list(perm)
           for n, perm in enumerate(itertools.permutations(range(5))))

assert all(nth_permutation_from_elements(n, [0,1,2,3,4]) == list(perm)
           for n, perm in enumerate(itertools.permutations(range(5))))
